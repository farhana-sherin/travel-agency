function toggleDescription(button) {
  const card = button.closest(".destination-card");
  const desc = card.querySelector(".description");
  const arrow = button.querySelector(".arrow-icon");

  // Only toggle current card's description
  if (desc.style.maxHeight && desc.style.maxHeight !== "0px") {
    desc.style.maxHeight = "0";
    arrow.classList.remove('rotate-180');
  } else {
    desc.style.maxHeight = desc.scrollHeight + "px";
    arrow.classList.add('rotate-180');
  }
}
