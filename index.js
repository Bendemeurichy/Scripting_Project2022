const knop=document.querySelector("#toevoegKnop");
const eindveld = document.querySelector("#eindpunt");

function getinfo(lang, start, stop) {
    knop.disabled=true;
    const items = document.querySelectorAll("#items li");
    const huidigeLijst = [];
    for (let item of items) {
        huidigeLijst.push(item.innerText);
    }
    const data = {lijst: huidigeLijst};
    fetch(`cgi-bin/wiki.py?lang=${lang}&start=${start}&stop=${stop}`)
        .then(antwoord => antwoord.json()).then(knop.disabled=true).then(data => {
        let html = "";
        if(data["paths"]===undefined){
            
            alert(data["error"])
        } else {
            for (let item of data["paths"]) {
                html += `<li>${item}</li>`;
            }
            document.querySelector("#items").innerHTML = html;
        }
        knop.disabled = false
    });

}

knop.addEventListener("click", () => {
    const lang = document.querySelector("#taal").value || "en";
    const start = document.querySelector("#start").value || "Special:Random";
    const stop = eindveld.value || "Philosophy";
    getinfo(lang, start, stop);
});

eindveld.addEventListener("input", ()=> {
    document.querySelector("#items").innerHTML = `<li>${eindveld.value||"Philosophy"}</li>`;
});

document.querySelector("#taal").addEventListener("input",()=>{
    document.querySelector("#items").innerHTML = `<li>${eindveld.value||"Philosophy"}</li>`;
});
