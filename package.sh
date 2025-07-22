PACKAGES=cnx-fsw-application-curl

USAGE="""Usage : package.sh [PACKAGE_NAME [VERSION]]
	Construit le(s) package(s) rpm : $PACKAGES
	en se basant sur les fichiers de spec dans packaging/
	La version du package est déterminée dans le fichier de spec. La release du package est déterminée automatiquement.
	Par défaut (i.e: sans paramètres) construit avec le commit courant puis tague celui-ci avec : "version-release"
	Si le dépôt git donne lieu à plusieurs packages, le tag est de la forme : "package_name-version-release"
	PACKAGE_NAME : Nom du package à construire
	VERSION : Numéro de version à construire (après l'avoir "checkoutée")
"""
[[ "$1" == "--help" ]] && echo -e "$USAGE" && exit 0
[[ "$1" != "" ]] && PACKAGES=$1  # On réécrit la liste des packages à construire avec seulement le package donné en paramètre
[[ "$(grep , <(echo $PACKAGES))" != "" ]] && tag_pack=${package_name}-    # On détecte s'il y a plusieurs packages à construire, dans ce cas on préfixera le nom des tags
arg_version=$2

for package in `echo $PACKAGES | sed 's/,/ /g'`;
do

if [[ "$arg_version" == "" ]]; then  # Si la version n'a pas été précisée en paramètre, c'est qu'on veut créer une nouveau package avec le commit courant
	rm -Rf "./rpmbuild"

	# Le n° de version à construire est celui du fichier spec.
	spec_version=$(grep -Po "Version:[ \t]*[0-9.]*" packaging/$package.spec | awk '{print $2}')

	# enlève localement les tags deleted sur la branch remote
	git fetch --prune origin +refs/tags/*:refs/tags/*

	# hash du commit courant
	git_hash=$(git log --abbrev-commit --decorate | grep "(HEAD\| HEAD" | awk '{print $2}')

	# La dernière release construite pour cette version.
	last_release=$(git log --abbrev-commit --decorate | grep -Po "tag: ${tag_pack}${spec_version}-[0-9]*" | sort -rV | head -n 1 | sed 's/tag: '${tag_pack}${spec_version}'-\([0-9]*\).*/\1/g')	
	# Le hash de la dernière release construite.
	last_release_hash=$(git log --abbrev-commit --decorate | grep "tag: ${tag_pack}${spec_version}-${last_release}" | awk '{print $2}')

	if [[ "$last_release_hash" == "$git_hash" ]]; then   # Le commit courant a déjà été construit (peut-être sur une autre distrib), c'est qu'on veut créer un même package sur une autre distrib, on garde alors le numéro de release.
		release_to_build=$last_release
	else		# Note : s'il n'y a pas eu d'autre release déjà construite, last_release est vide et la ligne ci-dessous donnera release_to_build=1 
		release_to_build=$((last_release+1)) 
	fi

else  # Si la version est précisée, c'est qu'on veut reconstruire une version déjà taguée. En $2 est précisé le nom du package.
	version=$(echo $arg_version | awk 'BEGIN{FS="-"}{print $1}')
	release_to_build=$(echo $arg_version | awk 'BEGIN{FS="-"}{print $2}')
#	[[ "$spec_version" != "$version" ]] && echo "ERREUR : Version dans fichier .spec $spec_version différent du version du tag" >&2 && exit 1
	echo "$version - $release_to_build"
	git checkout $tag_pack$arg_version
fi

# On vérifie qu'un autre commit que le commit courant n'ait pas déjà été tagué avec cette version-release
tag_commit=$(git log --abbrev-commit --decorate | grep "tag: ${tag_pack}${spec_version}-${release_to_build}" | grep -v "(HEAD\| HEAD")
if [[ "$tag_commit" != "" ]]; then
	echo "ERREUR : Il y a déjà un commit tagué ${tag_pack}${spec_version}-${release_to_build} : $tag_commit" >&2
	exit 1
fi

### Partie spécifique à ce dépôt (Attention à bien gérer le cas de multi-packages) ###
### Fin ###

# Création du package, cette ligne se lance à la racine du dépôt git et crée une arbo sous rpmbuild
rpmbuild -bb packaging/${package}.spec --define "_topdir `pwd`/rpmbuild" --define "_iv_pkg_release ${release_to_build}" --define "gitdir `pwd`"

[[ $? != 0 ]] && echo "Des erreurs, je ne tague rien" && exit

git tag ${tag_pack}${spec_version}-${release_to_build} 2>/dev/null   # Si on relance le même build sur le même commit on a un fatal tag exists
git push --tags

done
