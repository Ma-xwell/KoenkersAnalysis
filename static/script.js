const formNames = document.getElementById("formNames");
const formFactors = document.getElementById("formFactors");
var newname2, newname3;
var formNamesSubmitted = false;

// Changing names of the factors
formNames.addEventListener("submit", function(event) {
    event.preventDefault();
    newname2 = document.getElementById("name2").value;
    newname3 = document.getElementById("name3").value;
    var names2 = document.getElementsByClassName("newname2");
    var names3 = document.getElementsByClassName("newname3");
    for (let i = 0; i < names2.length; i++){
        names2[i].innerHTML = newname2;
        names3[i].innerHTML = newname3;
    }
    formNamesSubmitted = true;
});

// Passing the custom names of the factors to the proper form so they will be POSTed into Flask endpoint
formNames.addEventListener("submit", function() {
    document.getElementById("_name2").value = document.getElementById("name2").value;
    document.getElementById("_name3").value = document.getElementById("name3").value;
});


// Checking if factors are named and if the price is not the same
formFactors.addEventListener("submit", function(event) {
    if (!formNamesSubmitted){
        event.preventDefault();
    }
    priceyou = document.getElementById("priceyou").value
    pricecomp = document.getElementById("pricecomp").value

    if (priceyou == pricecomp){
        window.alert("Prices cannot be the same.")
        event.preventDefault();
    }
});

// Resets formNames and formFactors when page refreshed
window.onbeforeunload = function() {
    document.getElementById("formNames").reset();
    document.getElementById("formFactors").reset();
}