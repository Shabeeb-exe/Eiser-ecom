$(document).ready(function(){
    //homepage banner slick-slider
    $('.slider').slick({
        dots: true,
        infinite: true,
        speed: 500,
        arrows: true,
        autoplay: true,
        autoplaySpeed: 5000,
        cssEase: 'linear'
    });
    
    // Initialize product carousel only if there are more than 3 products
    $('.product-carousel').each(function () {
        if ($(this).children().length > 3) {
            $(this).slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                autoplay: false,
                arrows: true,
                dots: false,
                responsive: [
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1
                        }
                    }
                ]
            });
        }
    });
});