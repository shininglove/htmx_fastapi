<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>HTMX Shell</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="/static/output.css" />
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
        <link href="/static/video-js.css" rel="stylesheet" />
        <script src="/static/htmx.min.js"></script>
    </head>
    <body class="mx-auto container">
        <div class="bg-white p-2">
            <p class="text-slate-900 font-extrabold text-4xl cursor-pointer">
                $title
            </p>
            <form onsubmit="event.preventDefault()">
                <input
                    id="dir_search"
                    type="text"
                    name="search"
                    class="border-4 border-purple-400 mt-2 w-1/3 p-2"
                    hx-post="/filesystem"
                    hx-trigger="load, click from:#desktop"
                    hx-target="#folder_files"
                    value="$home"
                />
            </form>
            <section class="mt-2" id="">(⌐■_■)</section>
            <section class="mt-2" id="video_player">(づ ◕‿◕ )づ</section>
            <button
                id="move_folders"
                class="mt-3 p-3 rounded border border-purple-500 bg-purple-500 text-white font-extrabold"
                hx-post="/move_mode"
                hx-trigger="click"
                hx-target="#video_player"
            >
                Toggle Move
            </button>
            <button
                id="desktop"
                class="mt-3 p-3 rounded border border-yellow-500 bg-orange-500 font-extrabold"
            >
                Fetch Files
            </button>
            <button
                id="changemenu"
                class="mt-3 p-3 rounded border border-red-500 bg-pink-500 font-extrabold"
            >
                💁🏽
            </button>
        </div>
        <div class="flex pb-2">
            <section class="mt-2 gap-4 inline-flex flex-wrap" id="folder_files">
                -
            </section>
        </div>
    </body>
</html>
