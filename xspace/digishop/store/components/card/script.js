// var viewAllButtonA = document.getElementById('viewAllButA');
// var showLessButtonA = document.getElementById('showLessButA');
// var pagiButtonA = document.getElementById('pagiButA');
// var chevronButtonA = document.getElementById('chevronButA');
// var slider = document.getElementById('slider');
// var slidercontainer = document.getElementById('slider-container');
// var pagiLinkA = document.getElementsByClassName('pagiLink');
// const locoStorage = localStorage.getItem('viewAll');


// if(window.performance.navigation.type===0) {
//     if (locoStorage > 0) {
//         Stable();
//     } else {
//         Showless();
//     }
// };


(function(){
    document.getElementById('viewAllBut').onclick = function(){
        console.log('Stable');
        document.getElementById('viewAllBut').classList.add('hidden');
        document.getElementById('normalCardSlide').classList.add('hidden');
    }
}());


// viewAllButtonA.addEventListener('click', Stable);
// showLessButtonA.addEventListener('click', Showless);



// function Stable(){
//     console.log('Stable');
//     viewAllButtonA.classList.add('hidden');
//     chevronButtonA.classList.add('hidden');
//     // Remove the 'hidden' class from showLessButtonA and pagiButtonA
//     showLessButtonA.classList.remove('hidden');
//     pagiButtonA.classList.remove('hidden');

//     slider.classList.add('hidden');
//     spareslider.classList.remove('hidden');

//     localStorage.setItem('viewAll', '1');
//     console.log(locoStorage);
// }


// function Showless(){
//     window.location.reload();
//     console.log('Showless function run!');
//     localStorage.setItem('viewAll', '0');
//     console.log(locoStorage);
// }



// document.addEventListener("DOMContentLoaded", function() {
//     const paginationLinks = document.querySelectorAll('.pagiLinkA');

//     paginationLinks.forEach(link => {
//         link.addEventListener('click', function() {
//             Stable();
//             console.log('Page number selected:', pageNumber);
            
//         });
//     });
// });
