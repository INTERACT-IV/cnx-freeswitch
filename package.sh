PACKAGE=cnx-fsw-application-curl

# Le n° de version à construire est celui du fichier spec.
spec_version=$(grep -Po "Version:[ \t]*[0-9.]*" packaging/$PACKAGE.spec | awk '{print $2}')

if [[ "$1" == "" ]]; then  # Si on ne précise pas la version, c'est qu'on veut créer une nouveau package avec le commit courant
	rm -Rf "./rpmbuild"

	# enlève localement les tags deleted sur la branch remote
	git fetch --prune origin +refs/tags/*:refs/tags/*

	# hash du commit courant
	git_hash=$(git log --abbrev-commit --decorate | grep "(HEAD\| HEAD" | awk '{print $2}')

	# La dernière release construite pour cette version.
	last_release=$(git log --abbrev-commit --decorate | grep -Po "tag: ${spec_version}-[0-9]*" | sort -rV | head -n 1 | sed 's/tag: '${spec_version}'-\([0-9]*\).*/\1/g')	
	# Le hash de la dernière release construite.
	last_release_hash=$(git log --abbrev-commit --decorate | grep "tag: ${spec_version}-${last_release}" | awk '{print $2}')

	if [[ "$last_release_hash" == "$git_hash" ]]; then
		release_to_build=$last_release
	else
		# Note : s'il n'y a pas eu de release déjà construite, last_release est vide et la ligne ci-dessous donnera release_to_build=1 
		release_to_build=$((last_release+1)) 
	fi

else  # Si la version est précisée, c'est qu'on veut reconstruire une version déjà taguée.
	version=$(echo $1 | awk 'BEGIN{FS="-"}{print $1}')
	release_to_build=$(echo $1 | awk 'BEGIN{FS="-"}{print $2}')
	[[ "$spec_version" != "$version" ]] && echo "ERREUR : Version dans fichier .spec $spec_version différent du version du tag" >&2 && exit 1
	echo "$version - $release_to_build"
	git checkout $1
fi

# On vérifie qu'un autre commit que le commit courant n'ait pas déjà été tagué avec cette version-release
tag_commit=$(git log --abbrev-commit --decorate | grep "tag: ${spec_version}-${release_to_build}" | grep -v "(HEAD\| HEAD")
if [[ "$tag_commit" != "" ]]; then
	echo "ERREUR : Il y a déjà un commit tagué ${spec_version}-${release_to_build} : $tag_commit" >&2
	exit 1
fi

### Partie spécifique à ce dépôt ###
### Fin ###

# Création du package, cette ligne se lance à la racine du dépôt git et crée une arbo sous rpmbuild
rpmbuild -bb packaging/${PACKAGE}.spec --define "_topdir `pwd`/rpmbuild" --define "_iv_pkg_release ${release_to_build}" --define "gitdir `pwd`"

# [[ $? != 0 ]] && echo "Des erreurs, je ne tague rien" && exit

#git tag ${spec_version}-${release_to_build} 2>/dev/null   # Si on relance le même build sur le même commit on a un fatal tag exists : on ignore
#git push --tags

