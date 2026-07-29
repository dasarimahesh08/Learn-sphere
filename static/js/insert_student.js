let sname = document.getElementById("sfn");
let email = document.getElementById("se");
let mobile = document.getElementById("smbn");
let dob = document.getElementById("dob");
let gender = document.getElementById("gn");
let age = document.getElementById("age");
let address = document.getElementById("ad");
let username = document.getElementById("un");
let password = document.getElementById("pw");
let confirmpassword = document.getElementById("cpw");
let selectedcourse = document.getElementById("course");
let trainer = document.getElementById("tnrs");
let registerbtn = document.getElementById("form");

// password strength fetcing
let pwcontent = document.getElementById("pw-strength");
let box1 = document.getElementById("box-1");
let box2 = document.getElementById("box-2");
let box3 = document.getElementById("box-3");
let lower = document.getElementById("lower");
let upper = document.getElementById("upper");
let numbers = document.getElementById("numbers");
let specialchar = document.getElementById("spechar");
let char8 = document.getElementById("8char");

// errors showing msgs fetching
let nameError = document.getElementById("name-error");
let emailError = document.getElementById("email-error");
let numError = document.getElementById("mob-error");
let dobError = document.getElementById("dob-error");
let gnError = document.getElementById("gn-error");
let ageError = document.getElementById("age-error");
let addressError = document.getElementById("ad-error");
let usernameError = document.getElementById("un-error");
let passwordError = document.getElementById("pw-error");
let confirmPwError = document.getElementById("cpw-error");
let courseError = document.getElementById("course-error");
let trainerError = document.getElementById("trainer-error");
let regError = document.getElementById("show-reg");

// get course 
selectedcourse.onchange = function (){
    let course = selectedcourse.value;
    fetch(`/get_trainers/${course}/`)
    .then(response => response.json())

    .then(data => {
        let trainerdetails = data.trainer;
        
        trainer.options.length = 0;

        let firstoption = new Option("Select trainer", "");

        trainer.add(firstoption);

        data.trainer.forEach(tnr => {

            let option =
            new Option(tnr.tname, tnr.tid);

            trainer.add(option);

        });
        
    });
}
pwcontent.style.display = "none";

password.onfocus = function(){
    pwcontent.style.display = "block";

}
password.onblur = function(){
    pwcontent.style.display = "none";
}

password.onkeyup = function(){
    let checkstrength = 0;

    let lowercheck = /[a-z]/;
    if (password.value.match(lowercheck)){
        lower.classList.remove("text-danger");
        lower.classList.add("text-success");
        checkstrength++
    } else{
        lower.classList.remove("text-success");
        lower.classList.add("text-danger");

    }
    let uppercheck = /[A-Z]/;
    if (password.value.match(uppercheck)){
        upper.classList.remove("text-danger");
        upper.classList.add("text-success");
        checkstrength++
    } else{
        upper.classList.remove("text-success");
        upper.classList.add("text-danger");
    }
    let numbercheck = /[0-9]/;
    if (password.value.match(numbercheck)){
        numbers.classList.remove("text-danger");
        numbers.classList.add("text-success");
        checkstrength++
    } else{
        numbers.classList.remove("text-success");
        numbers.classList.add("text-danger");
    }
    let specialcheck = /[!@#$%^&*]/;
    if (password.value.match(specialcheck)){
        specialchar.classList.remove("text-danger");
        specialchar.classList.add("text-success");
        checkstrength++
    } else{
        specialchar.classList.remove("text-success");
        specialchar.classList.add("text-danger");
    }
    if (password.value.length >=8){
        char8.classList.remove("text-danger");
        char8.classList.add("text-success");
        checkstrength++
    } else{
        char8.classList.remove("text-success");
        char8.classList.add("text-danger");
    }

    box1.classList.remove("bg-success" , "bg-warning" , "bg-danger")
    box2.classList.remove("bg-warning" , "bg-success");
    box3.classList.remove("bg-success");

    if (checkstrength<=2){
        box1.classList.add("bg-danger");
    } else if(checkstrength<=4){
        box1.classList.remove("bg-danger");
        box1.classList.add("bg-warning");
        box2.classList.add("bg-warning");
    } else if(checkstrength == 5){
        box1.classList.remove("bg-warning");
        box1.classList.add("bg-success");
        box2.classList.remove("bg-warning");
        box2.classList.add("bg-success");
        box3.classList.add("bg-success");
    }
}

registerbtn.addEventListener("submit" , function(e){
    let pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$/
    let namecheck = /^[A-Za-z\s]+$/
    let addcheck = /^[A-Za-z0-9\s,.\-\/#]+$/
    let isvalid = true

    nameError.innerText = ""
    emailError.innerText = ""
    numError.innerText = ""
    dobError.innerHTML = ""
    gnError.innerText = ""
    ageError.innerText = ""
    addressError.innerText = ""
    usernameError.innerText = ""
    passwordError.innerText = ""
    confirmPwError.innerText = ""
    courseError.innerText = ""
    trainerError.innerText = ""
    let emailval = email.value.trim()
    console.log(sname)
    console.log(nameError)
    console.log(sname.value)
    if (sname.value === ""){
        nameError.innerText = "Please enter your name"
        isvalid = false
    } else if(!(sname.value.match(namecheck))){
        nameError.innerText = "Please enter a valid name , the name should contain only alphabets"
        isvalid = false
    }
    if(emailval === ""){
        emailError.innerText = "Please enter your email"
        isvalid = false
    } else if (!emailval.endsWith("@gmail.com")){
        emailError.innerText = "Please enter a valid email id"
        isvalid = false
    }   
    let digitcheck = /[0-9]/
    if (mobile.value === ""){
       numError.innerText = "please enter your mobile number"
       isvalid = false
    } else if(!(mobile.value.match(digitcheck) && mobile.value.length == 10)){
        numError.innerText = "Please enter a valid phone number"
        isvalid = false
    }
    if (dob.value === ""){
        dobError.innerText = "Please enter your date of birth"
        isvalid = false
    }
    if (gender.value === ""){
        gnError.innerText = "Please select your gender"
        isvalid = false
    } 
    if (age.value === ""){
        ageError.innerText = "Please enter your age"
        isvalid = false
    } else if(!(age.value.match(digitcheck))){
        ageError.innerText = "Please enter valid age"
        isvalid = false
    }
    if (address.value === ""){
        addressError.innerHTML = "Please enter you address"
        isvalid = false
    } else if(!addcheck.test(address.value.trim())){
        addressError.innerText = "Please enter the valid address"
        isvalid = false
    }
    if (username.value === ""){
        usernameError.innerText = "Please enter your username"
        isvalid = false
    }
    if (password.value === ""){
        passwordError.innerText = "Please enter your password"
        isvalid = false
    } else if (!pattern.test(password.value)){
        passwordError.innerHTML = "Your password is too weak"
        isvalid = false
    }
    if (confirmpassword.value !== password.value){
        confirmPwError.innerText = "password and confirm password does not match"
        isvalid = false
    }
    if (selectedcourse.value === ""){
        courseError.innerText = "Please select your course"
        isvalid = false
    }
    if (trainer.value === ""){
        trainerError.innerText = "Please select trainer"
        isvalid = false
    }

    if(isvalid){
        registerbtn.submit();
    } else{
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