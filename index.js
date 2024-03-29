const knop=$("#toevoegKnop");
const eindveld = $("#eindpunt");
const inp=$("#input :input");

function getinfo(lang, start, stop) {
    const items = $("#items li");
    const huidigeLijst = [];
    for (let item of items) {
        huidigeLijst.push(item.innerText);
    }
    const old = {lijst: huidigeLijst};
    fetch(`cgi-bin/wiki.py?old=${JSON.stringify(old)}&lang=${lang}&start=${start}&stop=${stop}`)
        .then(antwoord => antwoord.json()).then(inp.prop("disabled",true)).then(data => {
        if(data["paths"]===undefined){
            inp.prop("disabled",false);
            alert(data["error"])
        } else {

            inp.prop("disabled",false);
            maketree(data["parent"],data["paths"])
        }

    })

}

//recursieve functie om tree toe te voegen aan bestaande html
function maketree(parent,addarray){
    if(addarray.length===1) {
        let el = addarray.shift();
        let par = document.getElementById(parent);
        $(par).append(`<li>${el}</li><ul id="${el}"></ul>`);
    } else {

        let el = addarray.shift();
        let par = document.getElementById(parent);
        $(par).append(`<li>${el}</li><ul id="${el}"></ul>`);
        return maketree(el,addarray);
    }
}

knop.click( () => {
    const lang = document.querySelector("#taal").value || "en";
    const start = document.querySelector("#start").value.replace(" ","_") || "Special:Random";
    const stop = document.querySelector("#eindpunt").value.replace(" ","_") || "Philosophy";
    getinfo(lang, start, stop);
});

eindveld.on("input",null,null,()=>{
    $("#items").html(`<li>${eindveld.val()||"Philosophy"}</li><ul id=${eindveld.val()||"Philosophy"}></ul>`);
});

$("#taal").on("input",null,null,()=>{
    $("#items").html(`<li>${eindveld.val()||"Philosophy"}</li><ul id=${eindveld.val()||"Philosophy"}></ul>`);
});

