'use strict';

const midContent = document.querySelector(".mid-content");
const h2LinkGithub = document.querySelector(".github-text");
const rightContent = document.querySelector('.right-content');
const content = document.querySelector('.mid-content');
const expandWrapper = document.querySelector('.expand-wrapper');
const body = document.querySelector('.main');
const rightBottomSection = document.querySelector('.right-bottom-content')
const modalWindow = document.querySelector('.modal')
const overlay = document.querySelector('.overlay')
const btnCloseModal = document.querySelector('.close-modal');


gsap.to(".main", { y: "300 ",ease: Power3.easeInOut, duration:1.3,opacity:1});

function githubLink(){
parent.open('https://github.com/Rezekne-Academy-of-Technologies/MQTT_Connector')
}
midContent.addEventListener("click",()=>{

    midContent.classList.toggle("expand");
    midContent.classList.toggle("mid-content");

    if(document.querySelector(".expand")){


        h2LinkGithub.style.fontSize = "13px";
        h2LinkGithub.style.transform = "rotate(-90deg)"
        h2LinkGithub.style.width = "100%";

        rightContent.style.display = "flex";
        rightContent.style.alignContent = 'center';
        rightContent.style.height="100%";
        rightContent.style.width="1%";

        content.innerHTML = `
             <div class="expand-wrapper">
             <div class="top-expand-section">
                          <h1>General</h1>
             </div>
             <div class="bottom-expand-section">
             <div class="left-column">
             <div>Name</div>
             <div>Client ID</div>
             <div>Host</div>
             <div>Port</div>
             <div>Username</div>
             <div>Password</div>
             </div>
             <div class="right-column">
             <div>rooms</div>
             <div>mqttx_0e0f6f72</div>
             <div>mqtt://192.168.69.2</div>
             <div>1883</div>
             <div>RTA_rooms</div>
             <div>RTA_rooms</div>
             </div>

             </div>`


    }
    else{
        h2LinkGithub.style.color = 'white'
        h2LinkGithub.style.fontSize = "40px";
        h2LinkGithub.style.transform = "rotate(0deg)"
        h2LinkGithub.style.width = "60%";

        rightContent.style.display = "flex";
        rightContent.style.alignContent = 'center';
        rightContent.style.justifyContent = 'center';

           content.innerHTML = `<div class="mid-upper">
                 <span class="dot-first"></span>
                 <span class="dot-second"></span>
                 <i class="arrow fa-sharp fa-solid fa-arrow-right"></i>
             </div>
             <div class="mid-middle">
                 <h1 class="h1-visible">SET THE CONNECTION TO MQTT X</h1>
             </div>
             <div class="mid-bottom">
             </div>`
    }

})
/*--------------------------MODAL-----------------------------------------*/
const closeModal = function () {
  modalWindow.classList.add('hidden');
  overlay.classList.add('hidden');

};

rightBottomSection.addEventListener('click',(e)=>{

    modalWindow.classList.toggle('hidden');
    overlay.classList.toggle('hidden');


    overlay.addEventListener('click',closeModal)
    modalWindow.addEventListener('click',closeModal)

})