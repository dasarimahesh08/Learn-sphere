        let currentpw = document.getElementById("ctpw");
        let newpw = document.getElementById("npw");
        let confirmpw = document.getElementById("cmpw");

        let checkBlock = document.getElementById("checking-block");
        let currentpwerror = document.getElementById("current-pw-error");
        let char8 = document.getElementById("characters");
        let lowercase = document.getElementById("lowercase");
        let uppercase = document.getElementById("uppercase");
        let number = document.getElementById("numbers");
        let spechar = document.getElementById("spe-char");
        let update = document.getElementById("update-form");
        let newPwError = document.getElementById("new-pw-error");
        let box1 = document.getElementById("strength-box-1");
        let box2 = document.getElementById("strength-box-2");
        let box3 = document.getElementById("strength-box-3");
        let cmpwerror = document.getElementById("cmpw-error");

        checkBlock.style.display = "none";
        
        newpw.onfocus = function(){
            checkBlock.style.display = "block";
        };

        newpw.onblur = function(){
            checkBlock.style.display = "none"
        }

        

        newpw.onkeyup = function()
        {
            let showstrength = 0;

            let lowerCaseLetters = /[a-z]/g;
            if (newpw.value.match(lowerCaseLetters)){
                lowercase.classList.remove("invalid")
                lowercase.classList.add("valid")
                showstrength++;

            }else{
                lowercase.classList.remove("valid");
                lowercase.classList.add("invalid")

            }
            let upperCaseLetters = /[A-Z]/g;
            if (newpw.value.match(upperCaseLetters)){
                uppercase.classList.remove("invalid")
                uppercase.classList.add("valid")
                showstrength++;
            }else{
                uppercase.classList.remove("valid")
                uppercase.classList.add("invalid")

            }
            let numbersCheck = /[0-9]/g;
            if (newpw.value.match(numbersCheck)){
                number.classList.remove("invalid")
                number.classList.add("valid")
                showstrength++;
            }else{
                number.classList.remove("valid")
                number.classList.add("invalid")

            }
            let specialSymbols = /[!@#$%^&*]/g;
            if (newpw.value.match(specialSymbols)){
                spechar.classList.remove("invalid")
                spechar.classList.add("valid")
                showstrength++;
            }else{
                spechar.classList.remove("valid")
                spechar.classList.add("invalid")
 
            }
            if (newpw.value.length>=8){
                char8.classList.remove("invalid")
                char8.classList.add("valid")
                showstrength++;
            }else{
                char8.classList.remove("valid")
                char8.classList.add("invalid")
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
           
        update.addEventListener("submit" , function(e){
            
            let pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/

            currentpwerror.innerText = "";
            newPwError.innerText = "";
            cmpwerror.innerText = "";

            let isvalid = true
            if(currentpw.value.trim() === "")
            {
                currentpwerror.innerText = "please enter the current password";
                isvalid = false
            }
            if (newpw.value.trim() === "")
            {
                newPwError.innerHTML = "please enter the new password"
                isvalid = false
            } else if (pattern.test(newpw.value.trim()))
            {
                pwval = newpw.value;
            } else
            {
                newPwError.innerHTML = "The password strength is too Less "
                isvalid = false
            }
            if (newpw.value.trim() !== confirmpw.value.trim()){
                cmpwerror.innerText = "Confirm password doesnot match";
                isvalid = false
            } else
            {
                cmpwval = confirmpw.value; 
            }
            if(!isvalid){
                e.preventDefault()
            }
        
        });
