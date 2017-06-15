echo "Commit message: "
read message
git commit -a -m "$message"
git push
