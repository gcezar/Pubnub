// Init PubNub

var p = PUBNUB.init({
  subscribe_key: 'pub-c-b4be713a-be4f-4872-b5c8-6232f76df1d4',
  publish_key:   'sub-c-f271816a-f3c4-11e6-88c3-0619f8945a4f'
});

// Sending data

function subcircuit() {
  p.publish({
    channel : 'RMBX-Office', // This is the channel name you are subscribing in remote-led.py
    message : {led: 1}
  });
}

// Click event
document.querySelector('button').addEventListener('click', subcircuit);
