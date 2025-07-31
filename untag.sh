# Retire un tag localement et sur le dépôt distant
git tag -d $1
git push origin :$1
