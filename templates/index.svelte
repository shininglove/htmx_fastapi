<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>HTMX Shell</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="/static/output.css" />
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
        <script src="/static/htmx.min.js"></script>
    </head>
    <body class="mx-auto container">
        <div class="sticky top-0 bg-white p-2">
            <p class="text-red-500 font-extrabold text-4xl">$homies</p>
            <form onsubmit="event.preventDefault()">
                <input
                    id="dir_search"
                    type="text"
                    name="search"
                    class="border-2 border-orange-400 mt-2 w-1/3 p-2"
                    hx-post="/filesystem"
                    hx-trigger="load, click from:#desktop"
                    hx-target="#folder_files"
                    value="$home"
                />
            </form>
            <section class="mt-2" id="video_player">-</section>
            <button
                id="desktop"
                class="mt-3 p-3 rounded border border-yellow-500 bg-orange-500 font-extrabold"
            >
                Fetch Files
            </button>
            <button
                id="rename"
                class="mt-3 p-3 rounded border border-purple-500 bg-purple-500 font-extrabold"
            >
                Rename Folder
            </button>
            <button
                id="new_folder"
                class="mt-3 p-3 rounded border border-pink-500 bg-red-500 font-extrabold"
            >
                New Folder
            </button>
        </div>
        <div class="flex pb-2">
            <section class="mt-2 gap-4 inline-flex flex-wrap" id="folder_files">
                -
            </section>
        </div>
    </body>
</html>
