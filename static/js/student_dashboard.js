let profilebtn = document.getElementById("profilebtn");
let popup = document.getElementById("parent-popup");
let closebtn = document.getElementById("closebtn");

let changePwBtn = document.getElementById("change-pw-btn");
let logoutBtn = document.getElementById("logout-btn");

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


