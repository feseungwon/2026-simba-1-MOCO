const startBtn = document.querySelector('.start_btn');
const modalOverlay = document.getElementById('modal-overlay');
const modalMessage = document.getElementById('modal-message');
const modalClose = document.getElementById('modal-close');

function showModal(message) {
    modalMessage.textContent = message;
    modalOverlay.classList.remove('hidden');
}

modalClose.addEventListener('click', () => {
    modalOverlay.classList.add('hidden');
});

modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) modalOverlay.classList.add('hidden');
});

function getSelectedCategoryItemCount() {
    const categoryId = document.getElementById('selected_category').value;
    if (categoryId === '') return TOTAL_ITEM_COUNT;
    return CATEGORY_ITEM_COUNTS[categoryId] ?? 0;
}

function updateStartBtn() {
    const size = document.getElementById('selected_size').value;
    const categorySelected = document.querySelector('.category_btn.selected') !== null;
    startBtn.disabled = !(categorySelected && size);
}

function validateSelection() {
    const categoryBtn = document.querySelector('.category_btn.selected');
    const sizeBtn = document.querySelector('.round_btn.selected');

    if (!categoryBtn || !sizeBtn) return;

    const itemCount = getSelectedCategoryItemCount();

    if (itemCount === 0) {
        showModal('해당 카테고리에 아이템이 없습니다.');
        return;
    }

    const size = parseInt(document.getElementById('selected_size').value);
    if (size && itemCount < size) {
        showModal(`${size}강을 진행하려면 ${size}개 이상의 아이템이 필요합니다. (현재 ${itemCount}개)`);
    }
}

document.querySelectorAll('.round_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.round_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');

        if (btn.dataset.size === 'random') {
            const sizes = [16, 32, 64];
            const randomSize = sizes[Math.floor(Math.random() * sizes.length)];
            document.getElementById('selected_size').value = randomSize;
        } else {
            document.getElementById('selected_size').value = btn.dataset.size;
        }
        updateStartBtn();
        validateSelection();
    });
});

document.querySelectorAll('.category_btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.category_btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');

        document.getElementById('selected_category').value = btn.dataset.categoryId;
        updateStartBtn();
        validateSelection();
    });
});
