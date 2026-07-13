// inputs fetching
let fullname = document.getElementById("sfn");
let username = document.getElementById("un");
let email = document.getElementById("se");
let phno = document.getElementById("phno");
let address = document.getElementById("add");
let age = document.getElementById("age");
let dob = document.getElementById("dob");

// error showing tags fetching
let fullnameerror = document.getElementById("sfn-error");
let usernameerror = document.getElementById("un-error");
let emailerror = document.getElementById("se-error");
let phoneerror = document.getElementById("phno-error");
let addresserror = document.getElementById("add-error");
let ageerror = document.getElementById("age-error");
let doberror = document.getElementById("dob-error");

let updateBtn = document.getElementById("form");

updateBtn.addEventListener("submit" , function(e){
    let isvalid = true;

    fullnameerror.innerText = ""
    usernameerror.innerText = ""
    emailerror.innerText = ""
    phoneerror.innerText = ""
    addresserror.innerText = ""
    ageerror.innerText = ""
    doberror.innerText = ""

    if (fullname.value === ""){
        fullnameerror.innerText = "Please enter your full name"
        isvalid = false
    }
    if (username.value === ""){
        usernameerror.innerText = "Please enter your user name"
        isvalid = false
    }
    if (email.value === ""){
        emailerror.innerText = "Please enter you email id"
        isvalid = false
    } 
    let phonepattern = /^[0-9]+$/
    if (phno.value === ""){
        phoneerror.innerText = "Please enter your phone number"
        isvalid = false;
    } else if(!(phonepattern.test(phno.value) && phno.value.length == 10)){
        phoneerror.innerText = "Please enter valid phone number"
        isvalid = false;
    }
    if (address.value === ""){
        addresserror.innerText = "Please enter your address"
        isvalid = false;
    }
    if (age.value.length < 2){
        ageerror.innerText = "Please enter your age"
        isvalid = false;
    }
    if (dob.value === ""){
        doberror.innerText = "Please enter your date of birth"
        isvalid = false;
    }

    if(!isvalid){
        e.preventDefault()
    }


});

// profile popup for cropping the image

let profile = document.getElementById("profile");
let preview = document.getElementById("preview");
let profilepopup = document.getElementById("profile-popup");
let cropImage = document.getElementById("image");
profilepopup.style.display = "none";

profile.addEventListener("change" , function(){
    let pic = profile.files[0];
    if (pic){
        let imageURL = URL.createObjectURL(pic)
        cropImage.src = imageURL
        profilepopup.classList.remove("d-none")
    }
});

        let image = document.getElementById("image");
        let cropBtn = document.getElementById("cropBtn");

        let cropper;
        image.onload = function(){
             cropper = new Cropper(image , {
                aspectRatio: 1,
                viewMode: 1
            });
        }

        let previewBox = document.getElementById("preview");
        previewBox.style.display = "none"

        let previewImage = document.getElementById("previewImg");
        let croppedImage;
        cropBtn.addEventListener("click" , function(){
            // getting cropped image
            let canvas = cropper.getCroppedCanvas({
                width : 300 , 
                height : 300
            });

            //convert cropped image
            croppedImage = canvas.toDataURL('image/png');

            previewImage.src = croppedImage;

            previewBox.style.display = "block";
            console.log(croppedImage)
        });

        let saveBtn = document.getElementById("saveImg");

        saveBtn.addEventListener("click", function(){
            fetch(croppedImage)
            
            .then(res => res.blob())
            .then(blob => {
                let Filename = profile.files[0];

                let originalfilename = Filename.name;

                let file = new File([blob] , originalfilename , {type:"image/png"})

                let datatransfer = new DataTransfer();
                datatransfer.items.add(file);
                alert("image saved successfully")
                profile.files = datatransfer.files;
                console.log(profile.files[0]);
                profilepopup.classList.add("d-none")

            }); 
        });
