

function insertAd(ad, minParas, minWords){
    var paras = document.querySelectorAll("article p");
    var wordCount = 0
    var paraCount = 0
    var inserted = 0
    for (var i = 0; i < paras.length; i++){
        var p = paras[i];
        paraCount ++
        wordCount += p.innerText.length
        if (inserted >= 2){
            break
        }

        if (paraCount >= minParas && wordCount >= minWords) {
            console.log("find para", p)
            p.insertAdjacentHTML("afterend", ad)
            paraCount = 0
            wordCount = 0
            inserted += 1
        }
    }
    if (inserted == 0 & paras.length >= 5){
        var p = paras[paras.length - 1]
        p.insertAdjacentHTML("afterend", ad)
    }
}

document$.subscribe(function() {
    console.log("call in ad")
    fetch("/assets/ad/ad.txt").then(response =>{
        return response.text()
    }).then(ad =>{
        insertAd(ad, 30, 3000);
    })
})
