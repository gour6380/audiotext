import Vapor

// configures your application
public func configure(_ app: Application) async throws {

    // Increase the maximum body size to, 10MB
    app.routes.defaultMaxBodySize = "10mb"
    // register routes
    try routes(app)

}