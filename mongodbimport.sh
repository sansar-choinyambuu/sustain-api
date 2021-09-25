# import to mongodb cloud
cat ../data/products/de/*.json | ../mongodb-tools/bin/mongoimport --uri 'mongodb+srv://sustain:sustain@cluster0.rmjhl.mongodb.net/sustaindb?retryWrites=true&w=majority' --collection products
cat ../data/shoppingcart/*.csv | ../mongodb-tools/bin/mongoimport \
   --uri 'mongodb+srv://sustain:sustain@cluster0.rmjhl.mongodb.net/sustaindb?retryWrites=true&w=majority' \
   --collection='carts' \
   --type=csv \
   --fieldFile=fields.txt

# import to local mongodb
cat ../data/products/de/*.json | mongodb-tools/bin/mongoimport --host localhost --collection products
