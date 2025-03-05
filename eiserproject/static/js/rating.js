let star = document.querySelectorAll('input');
let showValue = document.querySelector('#rating-value');
let ratingDescription = document.querySelector('#ratingDescription');

let descriptions = {
    5: "Outstanding!",
    4.5: "Excellent!",
    4: "Very Good",
    3.5: "Good",
    3: "Average",
    2.5: "Below Average",
    2: "Poor",
    1.5: "Very Poor",
    1: "Terrible"
};

for (let i = 0; i < star.length; i++) {
    star[i].addEventListener('click', function() {
        let rating = this.value;  // Correctly reference this.value
        showValue.innerHTML = rating + " out of 5";
        ratingDescription.innerHTML = descriptions[rating];
    });
}