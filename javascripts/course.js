
var link="/articles/coursea/24lectures/intro/"
var img = "https://images.jieyu.ai/images/hot/course_promotion.jpg"

function insertAd(minParas, minWords){
    // 如果已经包含了链接，则不再增加，以允许手动增加
    var links = document.querySelectorAll("a[href*='" + link + "']");
    if (links.length > 0){
        console.log("已添加")
        return
    }

    var ad = "<p><a href='" + link + "'target='_blank'>" + "<img src='" + img + "'/>" + "</p>"

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
            console.log("find para", p, paraCount, wordCount)
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
    insertAd(40, 4000)
    // fetch("/assets/ad/ad.txt").then(response =>{
    //     return response.text()
    // }).then(ad =>{
    //     insertAd(ad, 30, 3000);
    // })
})