echo "Commit message: "
read message
git add ./_posts/*
git commit -a -m "$message"
git push
