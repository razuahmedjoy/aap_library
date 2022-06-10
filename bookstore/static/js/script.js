searchForm = document.querySelector('.searchbox');

document.querySelector('#search-btn').onclick = () => {
  searchForm.classList.toggle('active');

}

let loginForm = document.querySelector('.login-form-container');

// document.querySelector('#login-btn').onclick = () =>{
//   loginForm.classList.toggle('active');
// }

// document.querySelector('#close-login-btn').onclick = () =>{
//   loginForm.classList.remove('active');
// }

window.onscroll = () => {

  searchForm.classList.remove('active');

  if (window.scrollY > 80) {
    document.querySelector('.header .header-2').classList.add('active');
  } else {
    document.querySelector('.header .header-2').classList.remove('active');
  }

}



// window.onload = () =>{

//   if(window.scrollY > 80){
//     document.querySelector('.header .header-2').classList.add('active');
//   }else{
//     document.querySelector('.header .header-2').classList.remove('active');
//   }

//   fadeOut();

// }

// function loader(){
//   document.querySelector('.loader-container').classList.add('active');
// }

// function fadeOut(){
//   setTimeout(loader, 1000);
// }

var swiper = new Swiper(".books-slider", {
  loop: true,
  // centeredSlides: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});
var swiper = new Swiper(".slider-large", {
  loop: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  // autoplay: {
  //   delay: 4500,
  //   disableOnInteraction: false,
  // },
  breakpoints: {
    0: {
      slidesPerView: 2,
    },
    768: {
      slidesPerView: 3,
    },
    1024: {
      slidesPerView: 4,
    },
  },
});

var swiper = new Swiper(".featured-slider", {
  spaceBetween: 10,
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 9500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    450: {
      slidesPerView: 2,
    },
    768: {
      slidesPerView: 3,
    },
    1024: {
      slidesPerView: 4,
    },
  },
});

var swiper = new Swiper(".arrivals-slider", {
  spaceBetween: 10,
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 9500,
    disableOnInteraction: false,
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});
var swiper = new Swiper(".review-slider", {
  spaceBetween: 10,
  autoplay: {
    delay: 9500,
    disableOnInteraction: false,
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});

var swiper = new Swiper(".reviews-slider", {
  spaceBetween: 10,
  grabCursor: true,
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 9500,
    disableOnInteraction: false,
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});

var swiper = new Swiper(".blogs-slider", {
  spaceBetween: 10,
  grabCursor: true,
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 9500,
    disableOnInteraction: false,
  },
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});



// searchbox js

const search = document.getElementById('srch');
const results = document.querySelector('.results');

document.addEventListener("DOMContentLoaded", function () {


  search.onkeyup = () => {
    if (search.value.length >= 2) {

      const searchTxt = search.value;



      const getBooks = async () => {
        const url = "/search_books/"

        $.ajax({
          type: "POST",
          url: url,
          data: {
            'txt': searchTxt,
          },

          success: function (response) {
            // console.log(response);

            const { status, books } = response
            if (status == "success") {
              const bookList = JSON.parse(books);
              let innterList = ''
              if (bookList.length > 0) {

                for (let book of bookList) {

                  const { fields } = book;
                  innterList += `<li>
                      <a href="/book/${book.pk}/${fields.slug}">
                      <span name="title">
                         ${fields.title}
                        
                      </span>
                      <span class="price">bdt ${fields.price}</span>
                      </a>
                  </li>`


                }

              }
              else {
                innterList = `<li class="text-danger">
                No Books Found
            </li>`
              }

              results.innerHTML = innterList;
              results.classList.add('active')


            }
          },
          failure: function (e) {
            console.log(e)
          }


        })

      }
      getBooks();






    } else {


      results.classList.remove('active')
    }


  }


})






$("#search-box").keyup((e) => {
  const searchTxt = e.target.value;
  if (searchTxt.length >= 3) {
    const getBooks = async () => {
      const url = "/search_books/"

      $.ajax({
        type: "POST",
        url: url,
        data: {
          'txt': searchTxt,
        },

        success: function (response) {
          // console.log(response);

          const { status, books } = response
          if (status == "success") {
            const bookList = JSON.parse(books);
            for (book of bookList) {
              console.log(book.fields);
            }


          }
        },
        failure: function (e) {
          console.log(e)
        }


      })

    }
    getBooks();
  }

})



document.getElementById("searchBtn").addEventListener("click", (e) => {
  if(e.path[1].searchTxt.value.length > 1){

    e.path[1].submit();
  }else{
    alert("Please enter something to search")
  }
})
