document.addEventListener("DOMContentLoaded", function() {
  const wrapper = document.getElementById("wrapper");
  const wrap = document.getElementById("wrap");
  const register = document.getElementById("register");
  const login = document.getElementById("login");
  const regWrapper = document.getElementById("reg-wrapper");
  

  register.onclick=()=>{
    wrapper.style.visibility = "hidden";
    regWrapper.style.visibility = "visible";

    regWrapper.style.marginBottom = "70%";
    regWrapper.style.marginTop = "40%";
    wrap.style.height = "200vh";
  }

  login.onclick=()=>{
    wrapper.style.visibility = "visible";
    regWrapper.style.visibility = "hidden";
    wrap.style.height = "95vh";
    wrapper.style.marginTop = "170%";
    wrapper.style.marginBottom = "60%";
    
  }
});
