#!/bin/bash
cd /mnt/c/Users/rscdo/OneDrive/Desktop/NEA
git add .
git commit -m "Auto-update"
git pull origin main --rebase
git push origin main


