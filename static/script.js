function toggleDescription(button) {
  const card = button.closest(".destination-card");
  const desc = card.querySelector(".description");
  const text = button.querySelector(".toggle-text");
  const arrow = button.querySelector(".arrow-icon");

  // Toggle classes
  if (desc.classList.contains('max-h-0')) {
    desc.classList.remove('max-h-0');
    desc.classList.add('max-h-[200px]');
    arrow.classList.add('rotate-180');
    
  } else {
    desc.classList.remove('max-h-[200px]');
    desc.classList.add('max-h-0');
    arrow.classList.remove('rotate-180');
   
  }
}


