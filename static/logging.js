function logMessage(msg) {
        // This Part added to use with diffrent GoldHEN Payloads.
        const queryString = window.location.search;
        const url = new URL(window.location.origin +'/log/' + encodeURIComponent(msg));
        url.search=queryString;
        
        // const urlParams = new URLSearchParams(queryString);
        // urlParams.forEach((value,key) => {
        //         url.searchParams.set(key, value);
        // });
        // console.log(url);

        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onerror = function () {
                alert("Failed to log: message" + msg)
        }
        xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                //   console.log(xhr.response);
                  if (xhr.response!="OK"){
                        allset(xhr.response);
                  }
                }
              }
        xhr.on
        xhr.send();
}


