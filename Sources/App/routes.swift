import Vapor
import Foundation
import PythonKit

struct FileUpload: Content {
    var files: [File]
}

struct Config: Content {
    var enable_speaker_diarizations: Bool
    var diarization_speaker_counts: Int
    var language_codes: String
}

func getListOfAudioFiles() throws -> [String] {
    let fileManager = FileManager.default
    let publicDirectory = DirectoryConfiguration.detect().publicDirectory
    let audiosDirectory = publicDirectory.appending("audios/")

    guard let files = try? fileManager.contentsOfDirectory(atPath: audiosDirectory) else {
        throw Abort(.internalServerError, reason: "Unable to read files in audios directory")
    }

    return files.filter { $0.hasSuffix(".mp3") || $0.hasSuffix(".wav") } // Filter only audio files if needed
}

func getListOfAudioFilesabsolute() throws -> [String] {
    let fileManager = FileManager.default
    let publicDirectory = DirectoryConfiguration.detect().publicDirectory
    let audiosDirectory = publicDirectory.appending("audios/")

    guard let fileNames = try? fileManager.contentsOfDirectory(atPath: audiosDirectory) else {
        throw Abort(.internalServerError, reason: "Unable to read files in audios directory")
    }

    let audioFiles = fileNames.filter { $0.hasSuffix(".mp3") || $0.hasSuffix(".wav") }
    let absolutePaths = audioFiles.map { audiosDirectory.appending($0) }

    return absolutePaths
}


func routes(_ app: Application) throws {

    let subprocess = Python.import("subprocess")
    let os = Python.import("os")
    let sys = Python.import("sys")

    os.chdir("AudiotoText");

    // Get the current working directory directly, as it's not an Optional
    let cwd = os.getcwd()


    let install_lib = subprocess.run(["pip3", "install", "-e", "."])

    //Check if the command was successful
    if install_lib.returncode == 0 {
        print("Package installed successfully.")
    }
    else{
        print("Failed to install package.")
    }

    sys.path.append(cwd) // Add the path to your custom package
    let myAudiotoTextlib = Python.import("AudiotoText")

    app.get { req -> EventLoopFuture<View> in
        return req.view.render("index.html")
    }

    app.post("upload") { req -> Response in

        let directory = DirectoryConfiguration.detect().workingDirectory
        let audiosDirectory = directory.appending("Public/audios")

        // Create the "audios" directory if it doesn't exist
        if !FileManager.default.fileExists(atPath: audiosDirectory) {
            try FileManager.default.createDirectory(atPath: audiosDirectory, withIntermediateDirectories: true)
        }

        // Access uploaded files
        let upload = try req.content.decode(FileUpload.self)

        // Loop through uploaded files
        for file in upload.files {
            // Ensure the file has a valid file extension
            guard let ext = file.filename.split(separator: ".").last.map(String.init) else {
                throw Abort(.badRequest, reason: "Invalid file extension")
            }

            let validExtensions: Set<String> = ["mp3", "wav"]            

            guard validExtensions.contains(ext.lowercased()) else {
                throw Abort(.badRequest, reason: "Unsupported file type")
            }

            // Construct the file path
            let filePath = URL(fileURLWithPath: audiosDirectory).appendingPathComponent(file.filename)

            let fileData = Data(buffer: file.data)

            // Write the file data to the specified path
            try fileData.write(to: filePath)
        }

        do {
            let audioFiles = try getListOfAudioFiles() // Assuming you have this function
            var fileListHTML = ""

            for file in audioFiles {
                fileListHTML += "<li>\(file)</li>"
            }

            let resourcesDirectory = app.directory.resourcesDirectory
            let templatePath = resourcesDirectory + "Views/uploadSuccess.html"
            var htmlContent = try String(contentsOfFile: templatePath, encoding: .utf8)

            htmlContent = htmlContent.replacingOccurrences(of: "{{audioList}}", with: fileListHTML)

            // Create a custom response with the correct content type
            var headers = HTTPHeaders()
            headers.add(name: .contentType, value: "text/html")
            return Response(status: .ok, headers: headers, body: Response.Body(string: htmlContent))
        } catch {
            // Handle error
            let response = Response(status: .internalServerError, body: Response.Body(string: "Error: \(error)"))
            return response
        }
    }

    app.get("list") { req -> Response in
        do {
            let audioFiles = try getListOfAudioFiles() // Assuming you have this function
            var fileListHTML = ""

            for file in audioFiles {
                fileListHTML += "<li>\(file)</li>"
            }

            let resourcesDirectory = app.directory.resourcesDirectory
            let templatePath = resourcesDirectory + "Views/uploadSuccess.html"
            var htmlContent = try String(contentsOfFile: templatePath, encoding: .utf8)

            htmlContent = htmlContent.replacingOccurrences(of: "{{audioList}}", with: fileListHTML)

            // Create a custom response with the correct content type
            var headers = HTTPHeaders()
            headers.add(name: .contentType, value: "text/html")
            return Response(status: .ok, headers: headers, body: Response.Body(string: htmlContent))
        } catch {
            // Handle error
            let response = Response(status: .internalServerError, body: Response.Body(string: "Error: \(error)"))
            return response
        }
    }

    // Define the '/process' endpoint
    app.post("process") { req -> EventLoopFuture<String> in

        // Access config to process
        let upload = try req.content.decode(Config.self)

        let audioFiles = try getListOfAudioFilesabsolute()

        print(upload.enable_speaker_diarizations)

        let result = myAudiotoTextlib.main(audioFiles[0], upload.enable_speaker_diarizations, upload.diarization_speaker_counts, upload.language_codes)

        let extractedText = String(describing: result)

        return req.eventLoop.future(extractedText)
    }
}


func stringToBool(_ str: String) -> Bool? {
    switch str.lowercased() {
    case "true", "yes", "1":
        return true
    case "false", "no", "0":
        return false
    default:
        return nil  // or return a default value like `false` if you prefer
    }
}