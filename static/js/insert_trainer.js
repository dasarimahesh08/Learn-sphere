        let ddbtn = document.getElementById("dd-click");
        let ddcontent = document.getElementById("dd-content");
        let tpw = document.getElementById("pw");
        let strengthBlock = document.getElementById("strength-block");
        let box1 = document.getElementById("box-1");
        let box2 = document.getElementById("box-2");
        let box3 = document.getElementById("box-3");
        let lower = document.getElementById("lower");
        let upper = document.getElementById("upper");
        let special = document.getElementById("special");
        let number = document.getElementById("number");
        let char8 = document.getElementById("8char");
        let strengthCheckBlock = document.getElementById("pw-strength-check");
        let subBtn = document.getElementById("submit-btn");;
        let tname = document.getElementById("tfn");
        let email = document.getElementById("eml");
        let sal = document.getElementById("sal");
        let exp = document.getElementById("exp");
        let spe = document.getElementById("spe");
        let courses = document.querySelectorAll("input[name = 'courses']");
        let nameerror = document.getElementById("nameerror");
        let emailerror = document.getElementById("emailerror");
        let salerror = document.getElementById("salerror");
        let experror = document.getElementById("experror");
        let speerror = document.getElementById("speerror");
        let pwerror = document.getElementById("pw-error");
        let crserror = document.getElementById("crserror");


        box1.style.display = "none";
        box2.style.display = "none";
        box3.style.display = "none";
        strengthCheckBlock.style.display = "none";

        strengthBlock.style.display = "none";
        ddcontent.style.display = "none";
        
        ddbtn.addEventListener("click" , function(){
            ddcontent.style.display = "block";
           
        });

        tpw.onfocus = function(){
            box1.style.display = "block";
            box2.style.display = "block";
            box3.style.display = "block";
            strengthCheckBlock.style.display = "block";
        }

        tpw.onkeyup = function(){

            let showstrength = 0;

            let lowercheck = /[a-z]/g;
            if (tpw.value.match(lowercheck)){
                lower.classList.remove("text-danger")
                lower.classList.add("text-success")
                showstrength++
            }  else{
                lower.classList.remove("text-success")
                lower.classList.add("text-danger")
            }
            let uppercheck = /[A-Z]/g;
            if (tpw.value.match(uppercheck)){
                upper.classList.remove("text-danger")
                upper.classList.add("text-success")
                showstrength++
            } else{
                upper.classList.remove("text-success")
                upper.classList.add("text-danger")
            }
            let specialcheck = /[!@#$%^&*]/g;
            if (tpw.value.match(specialcheck)){
                special.classList.remove("text-danger")
                special.classList.add("text-success")
                showstrength++
            } else{
                special.classList.remove("text-success")
                special.classList.add("text-danger")
            }
            let numbercheck = /[0-9]/g;
            if (tpw.value.match(numbercheck)){
                number.classList.remove("text-danger")
                number.classList.add("text-success")
                showstrength++
            }  else{
                number.classList.remove("text-success")
                number.classList.add("text-danger")
            }
            if (tpw.value.length >= 8){
                char8.classList.remove("text-danger")
                char8.classList.add("text-success")
                showstrength++
            }  else{
                char8.classList.remove("text-success")
                char8.classList.add("text-danger")
            }

            box1.classList.remove("bg-danger" , "bg-warning" , "bg-success")
            box2.classList.remove("bg-warning" , "bg-success")
            box3.classList.remove("bg-success")

            if (showstrength <=2)
            {
                box1.classList.add("bg-danger")   
            } else if(showstrength <= 4)
            {
                box2.classList.add("bg-warning");
                box1.classList.add("bg-warning");
            } else if(showstrength == 5)
            {
                box3.classList.add("bg-success")
                box2.classList.add("bg-success")
                box1.classList.add("bg-success")
            }
        }

        tpw.onblur = function(){
            box1.style.display = "none";
            box2.style.display = "none";
            box3.style.display = "none";
            strengthCheckBlock.style.display = "none";

        }

        
        subBtn.addEventListener("click" , function(e){
            let isvalid = true
            let pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[!@#$%^&*]).{8,}$/
            let salcheck = /(?=.*[\d])/

            nameerror.innerText = ""
            emailerror.innerText = ""
            salerror.innerText = ""
            experror.innerText = ""
            speerror.innerText = ""
            pwerror.innerText = ""
            crserror.innerText = ""
            
            if (tname.value ===""){
                nameerror.innerText = "Please enter the your name"
                isvalid = false
            }
            if(email.value === ""){
                emailerror.innerText = "Please enter the email"
                isvalid = false
            }
            if(sal.value === ""){
                salerror.innerHTML = "Please enter the salary"
                isvalid = false
            }  else if(!(sal.value.match(salcheck))){
                salerror.innerText = "Please enter in valid format"
                isvalid = false
            }
            if (exp.value == ""){
                experror.innerText = "Please select your experience"
                isvalid = false
            }
            if (spe.value == ""){
                speerror.innerText = "Please enter the specialization"
                isvalid = false
            }
            if (tpw.value === ""){
               pwerror.innerText = "Please enter the password" 
               isvalid = false
            } else if(!(pattern.test(tpw.value.trim()))){
                pwerror.innerText = "Please enter the strong password"
                isvalid = false
            }
            let selectedlist = []
            for(i = 0 ; i<courses.length ; i++){
                if (courses[i].checked){
                    selectedlist.push(courses[i].value);
                }
            }
            if (selectedlist.length == 0){
                crserror.innerText = "Please select atleast one course"
                isvalid = false
            }
            
            if (!isvalid){
                e.preventDefault()
            }
        });

        // password hiding

        let hideBtn = document.getElementById("eye");

        hideBtn.addEventListener("click" , function(){
            if (tpw.type === "password"){
                tpw.type = "text"
                hideBtn.innerHTML = `<i class="bi bi-eye-slash"></i>`
            } else{
                tpw.type = "password"
                hideBtn.innerHTML = `<i class="bi bi-eye"></i>`
            }
        });

// profile popup for cropping the image
        let dropdown = document.getElementById("dropdown-div");

        let profile = document.getElementById("pic");
        let profilepopup = document.getElementById("profile-popup");
        let image = document.getElementById("image");

        profile.addEventListener("change" , function(){
            let pic = profile.files[0];
            if (pic){
                let imageURL = URL.createObjectURL(pic)
                image.src = imageURL
                profilepopup.classList.remove("d-none");
                dropdown.style.display = "none"

            }
        });

       
        let cropBtn = document.getElementById("cropBtn");

        let cropper;
        image.onload = function(){
            if (cropper){
                cropper.destroy();
            }
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
            if (!croppedImage){
                alert("please crop the image")
                return;
            }
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
                dropdown.style.display = "block"

            }); 
        });