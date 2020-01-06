/* eslint-disable no-param-reassign */
/* eslint-disable no-unused-vars */
/* eslint-disable no-multi-assign */
/* eslint-disable no-undef */
/* eslint-disable func-names */
const modalBtns = document.querySelectorAll('.modal-open');

modalBtns.forEach((btn) => {
  btn.onclick = function () {
    const modal = btn.getAttribute('data-modal');
    document.getElementById(modal).style.display = 'flex';
  };
});

const closeBtns = document.querySelectorAll('.close');

closeBtns.forEach((btn) => {
  btn.onclick = function () {
    const modal = btn.closest('.modal').style.display = 'none';
  };
});

window.onclick = function (e) {
  if (e.target.className === 'modal') {
    e.target.style.display = 'none';
  }
};
