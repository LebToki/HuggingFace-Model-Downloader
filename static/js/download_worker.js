onmessage = function(e) {
    const { model_name, action } = e.data;

    if (action === 'download') {
        importScripts('https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js');

        axios.post('/download_small_model', { model_name })
            .then(response => {
                postMessage({ status: 'success', model_name: model_name, message: response.data.message });
            })
            .catch(error => {
                postMessage({ status: 'error', model_name: model_name, message: error.response.data.error });
            });
    }
}
