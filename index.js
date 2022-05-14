function getinfo(lang, start, stop) {
    const items = document.querySelectorAll("#items li");
    const huidigeLijst = [];
    for (let item of items) {
        huidigeLijst.push(item.innerText);
    }
    const data = {lijst: huidigeLijst};
    fetch(`cgi-bin/wiki.py?lang=${lang}&start=${start}&stop=${stop}`)
        .then(antwoord => antwoord.json()).then(data => {
        let html = "";
        for (let item of data["paths"]) {
            html += `<li>${item}</li>`;
        }
        document.querySelector("#items").innerHTML = html;
    });
}

document.querySelector("#toevoegKnop").addEventListener("click", () => {
    const lang = document.querySelector("#taal").value === "" ? "en" : document.querySelector("#taal").value;
    const start = document.querySelector("#start").value === "" ? "Special:Random" : document.querySelector("#start").value.replaceAll(" ","_");
    const stop = document.querySelector("#eindpunt").value === "" ? "Philosophy" : document.querySelector("#eindpunt").value.replaceAll(" ","_");
    getinfo(lang, start, stop);
})