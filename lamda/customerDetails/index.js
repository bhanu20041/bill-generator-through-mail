const AWS = require("aws-sdk");
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = (event, context, callback) => {
    const tableName = "CustomerDetails";
    const params = {
        TableName: tableName,
        Item: {
            "customerId": event.customerId,
            "customerName": event.customerName,
            "items": event.items
        }
    };

    docClient.put(params, function (err, data) {
        if (err) {
            console.error("Error updating customer data:", err);
            callback(err, null); // Returning error
        } else {
            console.log("Successfully updated customer data");
            const response = {
                statusCode: 200,
                body: JSON.stringify({ message: 'Customer data stored successfully' })
            };
            callback(null, response); // Returning success response
        }
    });
};
