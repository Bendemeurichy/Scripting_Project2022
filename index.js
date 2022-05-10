function getinfo(lang,start,stop){
    fetch(`cgi-bin/wiki.py?lang=${lang}&start=${start}&stop=${stop}`);
}

document.querySelector("#toevoegKnop").addEventListener("click",()=>{
    const lang = document.querySelector("#taal").value===""?"en":document.querySelector("#taal").value;
    const start= document.querySelector("#start").value===""?"Special:Random":document.querySelector("#start").value;
    const stop=document.querySelector("#eindpunt").value===""?"Philosophy":document.querySelector("#eindpunt").value;
    getinfo(lang,start,stop);
})