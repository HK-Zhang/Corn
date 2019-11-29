function UpdateEnvironment(Env) {
    var collection = getContext().getCollection();

    // Query documents and take 1st item.
    var isAccepted = collection.queryDocuments(
        collection.getSelfLink(),
        'SELECT * FROM root r',
    function (err, feed, options) {
        if (err) throw err;

        // Check the feed and if empty, set the body to 'no docs found', 
        // else take 1st element from feed
        if (!feed || !feed.length) {
            var response = getContext().getResponse();
            response.setBody('no docs found');
        }
        else {

            for(var i=0;i<feed.length;i++){
                feed[i].environment=Env
                collection.replaceDocument(feed[i]._self,feed[i],function (err, itemReplaced) {
                if (err) throw "Unable to update, abort ";
                else console.log(itemReplaced.id+" get replaced")})
            }
        }
    });

    if (!isAccepted) throw new Error('The query was not accepted by the server.');
}