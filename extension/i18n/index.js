// i18n loader: t(key, params) resolving against extension/i18n/{en,es}.json.
// See docs/I18N_POLICY.md for the binding language policy.

let currentLocale = "en";
let dictionaries = { en: null, es: null };

function detectDefaultLocale() {
  const uiLang = chrome.i18n.getUILanguage();
  return uiLang.startsWith("es") ? "es" : "en";
}

async function loadDictionary(locale) {
  if (dictionaries[locale]) return dictionaries[locale];
  const url = chrome.runtime.getURL(`i18n/${locale}.json`);
  const response = await fetch(url);
  dictionaries[locale] = await response.json();
  return dictionaries[locale];
}

async function initLocale() {
  const stored = await chrome.storage.local.get("locale");
  currentLocale = stored.locale || detectDefaultLocale();
  await loadDictionary(currentLocale);
  return currentLocale;
}

async function setLocale(locale) {
  currentLocale = locale;
  await loadDictionary(locale);
  await chrome.storage.local.set({ locale });
}

function getLocale() {
  return currentLocale;
}

function t(key, params) {
  const dict = dictionaries[currentLocale] || {};
  if (dict[key] === undefined) {
    // Never fail silently: the key parity test should have caught this, so a
    // miss here means the dictionaries drifted after the last test run.
    console.warn(`[ventana] missing i18n key "${key}" for locale "${currentLocale}"`);
  }
  let text = dict[key] !== undefined ? dict[key] : key;
  if (params) {
    for (const [paramKey, value] of Object.entries(params)) {
      text = text.replace(`{${paramKey}}`, value);
    }
  }
  return text;
}
