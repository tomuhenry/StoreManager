function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle('active');
}

function redirectToAdmin(){
    // window.location.href="admin/index.html";
    // return true;
    document.getElementById("form-id").action = "../admin/";
}