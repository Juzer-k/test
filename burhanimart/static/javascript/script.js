console.log('hello');
$('.minus-cart-product').on('click',function () {
  console.log('hello');
  let id = $(this).attr("pid").toString();
  let product_quantity = this.parentNode.children[2];
  $.ajax(
    {
      type: "GET",
      url: "/minus-cart-product",
      data: {
        product_id: id
      },
      success: function (data) {
        console.log(data) 
        product_quantity.innerText = data.quantity;
        document.getElementById("amount").innerText = data.amount;
        document.getElementById("totalamount").innerText = data.totalamount;

      }
    })
});

$('.add-cart-product').click(function () {
  let id = $(this).attr("pid").toString();
  let product_quantity = this.parentNode.children[2];
  $.ajax(
    {
      type: "GET",
      url: "/add-cart-product",
      data: {
        product_id: id
      },
      success: function (data) {
        console.log(data)
        product_quantity.innerText = data.quantity;
        document.getElementById("amount").innerText = data.amount;
        document.getElementById("totalamount").innerText = data.totalamount;

      }
    })
});
$('.remove-cart-product').click(function () {
  let id = $(this).attr("pid").toString();
  let product_quantity = this;
  $.ajax(
    {
      type: "GET",
      url: "/remove-cart-product",
      data: {
        product_id: id
      },
      success: function (data) {
        console.log(data)
        // confirm('Are You Sure You Want To Remove This Porduct From Cart ?')
        product_quantity.parentNode.parentNode.parentNode.parentNode.remove()
      }
    })
});


/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
/* product detail slidershow container */
let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}



function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("demo");
  if (n > slides.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = slides.length }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
  captionText.innerHTML = dots[slideIndex - 1].alt;
}