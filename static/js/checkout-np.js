(function () {
  'use strict';

  var form = document.querySelector('[data-np-checkout]');
  if (!form) return;

  var configured = form.getAttribute('data-np-configured') === 'true';
  var citiesUrl = form.getAttribute('data-np-cities-url');
  var warehousesUrl = form.getAttribute('data-np-warehouses-url');
  var streetsUrl = form.getAttribute('data-np-streets-url');
  var methodAddress = form.getAttribute('data-method-address');

  var methodEl = document.getElementById('id_delivery_method');
  var cityEl = document.getElementById('id_delivery_city');
  var addressEl = document.getElementById('id_delivery_address');
  var houseEl = document.getElementById('id_house_number');
  var cityRefEl = document.getElementById('id_city_ref');
  var settlementRefEl = document.getElementById('id_settlement_ref');
  var citySuggest = document.getElementById('np-city-suggest');
  var secondarySuggest = document.getElementById('np-secondary-suggest');
  var houseWrap = document.querySelector('[data-np-house-wrap]');
  var addressLabel = document.querySelector('[data-np-address-label]');

  if (!methodEl || !cityEl || !addressEl || !citySuggest || !secondarySuggest) return;

  var cityTimer = null;
  var secondaryTimer = null;
  var activeRequest = 0;

  function isAddressMode() {
    return methodEl.value === methodAddress;
  }

  function hideSuggest(list) {
    list.hidden = true;
    list.innerHTML = '';
  }

  function syncMode(resetSecondary) {
    var addressMode = isAddressMode();
    if (houseWrap) {
      houseWrap.hidden = !addressMode;
    }
    if (addressLabel) {
      addressLabel.textContent = addressMode ? 'Вулиця' : 'Відділення';
    }
    addressEl.placeholder = addressMode
      ? 'Почніть вводити вулицю…'
      : 'Оберіть відділення…';
    if (resetSecondary) {
      addressEl.value = '';
      if (houseEl) houseEl.value = '';
      hideSuggest(secondarySuggest);
    }
  }

  function renderSuggest(list, items, onPick) {
    list.innerHTML = '';
    if (!items.length) {
      hideSuggest(list);
      return;
    }
    items.forEach(function (item, index) {
      var li = document.createElement('li');
      li.className = 'np-suggest__item';
      li.setAttribute('role', 'option');
      li.setAttribute('tabindex', '-1');
      li.textContent = item.label;
      li.addEventListener('mousedown', function (event) {
        event.preventDefault();
        onPick(item);
      });
      if (index === 0) li.classList.add('is-active');
      list.appendChild(li);
    });
    list.hidden = false;
  }

  function fetchJson(url) {
    var requestId = ++activeRequest;
    return fetch(url, {
      headers: { Accept: 'application/json' },
      credentials: 'same-origin',
    }).then(function (response) {
      return response.json().then(function (data) {
        return { requestId: requestId, ok: response.ok && data.ok, data: data };
      });
    });
  }

  function searchCities(query) {
    if (!configured || query.trim().length < 2) {
      hideSuggest(citySuggest);
      return;
    }
    var url = citiesUrl + '?q=' + encodeURIComponent(query.trim());
    fetchJson(url).then(function (result) {
      if (result.requestId !== activeRequest) return;
      if (!result.ok) {
        hideSuggest(citySuggest);
        return;
      }
      renderSuggest(citySuggest, result.data.results || [], function (item) {
        cityEl.value = item.city || item.label;
        if (cityRefEl) cityRefEl.value = item.city_ref || '';
        if (settlementRefEl) settlementRefEl.value = item.settlement_ref || '';
        hideSuggest(citySuggest);
        addressEl.value = '';
        if (houseEl) houseEl.value = '';
        hideSuggest(secondarySuggest);
        addressEl.focus();
        if (!isAddressMode()) {
          searchWarehouses('');
        }
      });
    }).catch(function () {
      hideSuggest(citySuggest);
    });
  }

  function searchWarehouses(query) {
    if (!configured || !cityRefEl || !cityRefEl.value) {
      hideSuggest(secondarySuggest);
      return;
    }
    var url = warehousesUrl
      + '?city_ref=' + encodeURIComponent(cityRefEl.value)
      + '&q=' + encodeURIComponent(query.trim());
    fetchJson(url).then(function (result) {
      if (!result.ok) {
        hideSuggest(secondarySuggest);
        return;
      }
      renderSuggest(secondarySuggest, result.data.results || [], function (item) {
        addressEl.value = item.label;
        hideSuggest(secondarySuggest);
      });
    }).catch(function () {
      hideSuggest(secondarySuggest);
    });
  }

  function searchStreets(query) {
    if (!configured || !settlementRefEl || !settlementRefEl.value || query.trim().length < 2) {
      hideSuggest(secondarySuggest);
      return;
    }
    var url = streetsUrl
      + '?settlement_ref=' + encodeURIComponent(settlementRefEl.value)
      + '&q=' + encodeURIComponent(query.trim());
    fetchJson(url).then(function (result) {
      if (!result.ok) {
        hideSuggest(secondarySuggest);
        return;
      }
      renderSuggest(secondarySuggest, result.data.results || [], function (item) {
        addressEl.value = item.label;
        hideSuggest(secondarySuggest);
        if (houseEl) houseEl.focus();
      });
    }).catch(function () {
      hideSuggest(secondarySuggest);
    });
  }

  methodEl.addEventListener('change', function () {
    syncMode(true);
  });

  cityEl.addEventListener('input', function () {
    if (cityRefEl) cityRefEl.value = '';
    if (settlementRefEl) settlementRefEl.value = '';
    clearTimeout(cityTimer);
    cityTimer = setTimeout(function () {
      searchCities(cityEl.value);
    }, 280);
  });

  cityEl.addEventListener('focus', function () {
    if (cityEl.value.trim().length >= 2 && cityRefEl && !cityRefEl.value) {
      searchCities(cityEl.value);
    }
  });

  addressEl.addEventListener('input', function () {
    clearTimeout(secondaryTimer);
    secondaryTimer = setTimeout(function () {
      if (isAddressMode()) {
        searchStreets(addressEl.value);
      } else {
        searchWarehouses(addressEl.value);
      }
    }, 280);
  });

  addressEl.addEventListener('focus', function () {
    if (!cityRefEl || !cityRefEl.value) return;
    if (isAddressMode()) {
      if (addressEl.value.trim().length >= 2) searchStreets(addressEl.value);
    } else {
      searchWarehouses(addressEl.value);
    }
  });

  document.addEventListener('click', function (event) {
    if (!form.contains(event.target)) {
      hideSuggest(citySuggest);
      hideSuggest(secondarySuggest);
    }
  });

  syncMode(false);
})();
