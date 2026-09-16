const list = document.querySelector('#participant-list');
const counter = document.querySelector('#participant-count');

function refreshParticipants() {
  if (!list || !counter) return;
  const rows = [...list.querySelectorAll('.participant-input')];
  counter.textContent = `${rows.length} added`;
  rows.forEach((row, index) => { row.querySelector('.person-index').textContent = String(index + 1).padStart(2, '0'); });
}

document.querySelector('#add-participant')?.addEventListener('click', () => {
  const row = document.createElement('div');
  row.className = 'participant-input';
  row.innerHTML = '<span class="person-index"></span><input name="participants" placeholder="Enter a name"><button type="button" class="icon-button remove-person" aria-label="Remove participant">×</button>';
  list.appendChild(row);
  row.querySelector('input').focus();
  refreshParticipants();
});

list?.addEventListener('click', (event) => {
  if (!event.target.classList.contains('remove-person')) return;
  const rows = list.querySelectorAll('.participant-input');
  if (rows.length > 1) event.target.closest('.participant-input').remove();
  refreshParticipants();
});
refreshParticipants();

const modal = document.querySelector('[data-payment-modal]');
document.querySelector('[data-open-payment]')?.addEventListener('click', () => modal?.classList.add('open'));
document.querySelector('[data-close-payment]')?.addEventListener('click', () => modal?.classList.remove('open'));
modal?.addEventListener('click', (event) => { if (event.target === modal) modal.classList.remove('open'); });

const importModal = document.querySelector('[data-import-modal]');
document.querySelector('[data-open-import]')?.addEventListener('click', () => importModal?.classList.add('open'));
document.querySelector('[data-close-import]')?.addEventListener('click', () => importModal?.classList.remove('open'));
importModal?.addEventListener('click', (event) => { if (event.target === importModal) importModal.classList.remove('open'); });

const settlementEditor = document.querySelector('[data-settlement-editor]');
const editorRows = settlementEditor?.querySelector('[data-editor-rows]');
const participantOptions = settlementEditor?.querySelector('[data-participant-options]')?.innerHTML || '';

document.querySelector('[data-toggle-editor]')?.addEventListener('click', () => settlementEditor.classList.toggle('open'));
settlementEditor?.addEventListener('click', (event) => {
  if (event.target.matches('.remove-transfer')) event.target.closest('.editor-row').remove();
  if (!event.target.matches('[data-add-transfer]')) return;
  const row = document.createElement('div');
  row.className = 'editor-row';
  row.innerHTML = `<select name="transfer_from" required>${participantOptions}</select><span>pays</span><select name="transfer_to" required>${participantOptions}</select><input name="transfer_amount" inputmode="decimal" placeholder="0.00" required><input type="hidden" name="transfer_original_amount" value=""><label class="settled-toggle"><input type="checkbox" name="transfer_settled" value="${editorRows.children.length}"><span>Settled</span></label><button class="icon-button remove-transfer" type="button" aria-label="Remove transfer">×</button>`;
  editorRows.appendChild(row);
});

settlementEditor?.addEventListener('change', (event) => {
  if (!event.target.matches('input[name="transfer_settled"]')) return;
  const row = event.target.closest('.editor-row');
  const amount = row.querySelector('input[name="transfer_amount"]');
  event.target.closest('.settled-toggle').classList.toggle('is-settled', event.target.checked);
  amount.readOnly = event.target.checked;
  if (event.target.checked) amount.value = '0.00';
});

settlementEditor?.querySelector('form')?.addEventListener('submit', () => {
  editorRows.querySelectorAll('.editor-row').forEach((row, index) => {
    row.querySelector('input[name="transfer_settled"]').value = String(index);
  });
});

document.querySelectorAll('[data-password-toggle]').forEach((toggle) => {
  toggle.addEventListener('click', () => {
    const input = toggle.closest('.password-field').querySelector('input');
    const visible = input.type === 'text';
    input.type = visible ? 'password' : 'text';
    toggle.setAttribute('aria-label', visible ? 'Show password' : 'Hide password');
    toggle.classList.toggle('is-visible', !visible);
  });
});