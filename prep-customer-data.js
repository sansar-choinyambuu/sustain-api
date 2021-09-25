const fs = require('fs');
const path = require('path');
const readline = require('readline');

const DATA_DIR = "../data"
const directory_path = path.join(DATA_DIR, "ShoppingCart");

console.log(directory_path);

var customers = [];

fs.readdir(directory_path, function (err, files) {
    if (err) {
        return console.err("Error reading directory!");
    }
    var allFiles = files.filter(f => f.endsWith(".csv"));
    processFiles(allFiles);
})

async function processFiles(files) {

    // for(var file in files){

    // }
    for(var i = 0; i < files.length; i++){
        var file = path.join(directory_path, files[i]);
        console.log(`Reading file ${file}`)
        const fileStream = fs.createReadStream(file);
        
        const rl = readline.createInterface({
            input: fileStream,
            crlfDelay: Infinity
        });
        
        var arr = [];
        var customer, purchase, timestamp_id, offset;
        for await (const line of rl) {
            if (line.startsWith("YYYYMM")) {
                continue;
            }

            arr = line.split(",");
            customer = customers.find(c => c.id === arr[1]);
            if (customer === undefined) {
                customer = {
                    "id": arr[1],
                    "purchases": []
                }
                customers.push(customer);
            }

            offset = arr[7].toString().length > 5 ? 1 : 0;
            timestamp_id = `${arr[6]} ${offset == 0 ? "0" : ""}${arr[7].toString().substr(0,1+offset)}:${arr[7].toString().substr(1+offset, 2)}:${arr[7].toString().substr(3+offset,2)}`

            purchase = customer.purchases.find(c => c.timestamp === timestamp_id);
            if (purchase === undefined) {
                purchase = {
                    "timestamp": timestamp_id,
                    "unix_timestamp": new Date(timestamp_id).getTime(),
                    "ProfitKSTID": arr[3],
                    "ProfitKSTNameD": arr[4],
                    "Genossenschaft": arr[5],
                    "products": [ ]
                }
                customer.purchases.push(purchase);
            }

            purchase.products.push({
                "product_id": arr[8],
                "amount": arr[9]
            })
        }
    }

    console.log("Writing Data");

    customers.forEach(c =>{
        var newFile = path.join(DATA_DIR, "customers", c.id + ".json");
        fs.writeFileSync(newFile, JSON.stringify(c), err => {
            if (err) {
                console.error(err)
                return
            }
            //file written successfully
        })
    });

    

}