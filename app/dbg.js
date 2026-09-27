window.addEventListener('error', function (e) {
  var x = e.error;
  console.log('ERR ' + String(x && x.dartException) + ' STACK ' + String(x && x.stack).slice(0, 1500).split(String.fromCharCode(10)).join(' | '));
});
