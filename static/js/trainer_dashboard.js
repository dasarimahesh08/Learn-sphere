
let profilebtn = document.getElementById("profilebtn")
let popup = document.getElementById("parent-popup")
let closebtn = document.getElementById("closebtn")

window.addEventListener( "pageshow" , function(e) {
        if( e.persisted || performance.navigation.type === 2 )
        {
            location.reload();
        }
    }
);

popup.style.display = 'none';
profilebtn.addEventListener("click" , function(){
    
        popup.style.display = 'block';
        closebtn.addEventListener("click" , function(){
            popup.style.display = 'none';
        });
});


let viewstdbtn = document.getElementById("std-btn");
let viewpopup = document.getElementById("view-std");
let closepopup = document.getElementById("close-btn");
console.log(viewstdbtn);
console.log(viewpopup);
console.log(closepopup);

viewpopup.style.display = 'none';

viewstdbtn.addEventListener("click" , function(){
   
    viewpopup.style.display = 'block';

    closepopup.addEventListener("click" , function(){
        viewpopup.style.display = 'none';
    });
});


// course popup

let courseBtn = document.getElementById("courseBtn");
let coursepopup = document.getElementById("course-popup");
let coursePopupclose = document.getElementById("course-close");

coursepopup.style.display = "none";
courseBtn.addEventListener("click" , function(){
    coursepopup.style.display = "block";
    coursePopupclose.addEventListener("click" , function(){
        coursepopup.style.display = "none";
    });
});