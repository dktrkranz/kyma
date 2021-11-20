module.exports = {
  main: function (event, context) {
    const {response} = event.extensions;
    response.setHeader("X-NetworkManager-Status", "online");
    return "X-NetworkManager-Status";
  }
}
