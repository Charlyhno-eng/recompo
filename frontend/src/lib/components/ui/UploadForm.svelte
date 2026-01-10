<script lang="ts">
    let {
        audioFile,
        videoFile,
        parts = $bindable(),
        language = $bindable(),
        minParts,
        maxParts,
        isLoading,
        currentSegment = 0,
        onAudioChange,
        onVideoChange,
        onSubmit,
    } = $props<{
        audioFile: File | null;
        videoFile: File | null;
        parts: number;
        language: "fr" | "en";
        minParts: number;
        maxParts: number;
        isLoading: boolean;
        currentSegment: number;
        onAudioChange: (e: Event) => void;
        onVideoChange: (e: Event) => void;
        onSubmit: (e: SubmitEvent) => void;
    }>();
</script>

<section class="flex-1 flex items-start justify-center">
    <div
        class="card w-full max-w-4xl mt-8 preset-filled-surface-900-950/80 border border-primary-500/40 shadow-2xl rounded-2xl p-8 sm:p-10 space-y-6 backdrop-blur"
    >
        <header class="space-y-2 text-left">
            <h1 class="text-3xl sm:text-4xl font-semibold text-white">
                Generation of subtitled videos
            </h1>
            <p class="text-sm sm:text-base text-surface-100/80 max-w-2xl">
                Add your audio, GIF or MP4, choose the number of videos, and
                we'll take care of the rest to create clips ready for social
                media.
            </p>
        </header>

        <form class="space-y-6" on:submit|preventDefault={onSubmit}>
            <div class="grid gap-6 md:grid-cols-2">
                <div class="space-y-2 text-left">
                    <label
                        for="audio"
                        class="block text-sm font-medium text-white"
                    >
                        Audio file (MP3)
                    </label>
                    <input
                        id="audio"
                        type="file"
                        accept="audio/mpeg,audio/mp3"
                        class="input w-full preset-outline-surface-50-900 bg-surface-900/70 border-surface-100/30 text-surface-50"
                        on:change={onAudioChange}
                        required
                        disabled={isLoading}
                    />
                    {#if audioFile}
                        <p class="text-xs text-surface-100/80">
                            Selected : {audioFile.name}
                        </p>
                    {/if}
                </div>

                <div class="space-y-2 text-left">
                    <label
                        for="video"
                        class="block text-sm font-medium text-white"
                    >
                        Visual file (MP4 or GIF)
                    </label>
                    <input
                        id="video"
                        type="file"
                        accept="video/mp4,image/gif"
                        class="input w-full preset-outline-surface-50-900 bg-surface-900/70 border-surface-100/30 text-surface-50"
                        on:change={onVideoChange}
                        required
                        disabled={isLoading}
                    />
                    {#if videoFile}
                        <p class="text-xs text-surface-100/80">
                            Selected : {videoFile.name}
                        </p>
                    {/if}
                </div>
            </div>

            <div class="space-y-2 text-left">
                <label
                    for="language"
                    class="block text-sm font-medium text-white"
                >
                    Subtitle language
                </label>
                <select
                    id="language"
                    class="input w-full preset-outline-surface-50-900 bg-surface-900/70 border-surface-100/30 text-surface-50"
                    bind:value={language}
                    disabled={isLoading}
                >
                    <option value="fr">French (default)</option>
                    <option value="en">English</option>
                </select>
                <p class="text-xs text-surface-100/80">
                    Choose the language used for the burned-in subtitles.
                </p>
            </div>

            <div class="space-y-3 text-left">
                <label for="parts" class="block text-sm font-medium text-white">
                    Number of videos to generate
                </label>
                <div class="flex items-center gap-4">
                    <input
                        id="parts"
                        type="range"
                        min={minParts}
                        max={maxParts}
                        bind:value={parts}
                        class="range flex-1 accent-primary-400"
                        disabled={isLoading}
                    />
                    <span
                        class="inline-flex items-center justify-center px-3 py-1 rounded-full bg-primary-500/80 text-sm font-semibold text-white"
                    >
                        {parts}
                    </span>
                </div>
                <p class="text-xs text-surface-100/80">
                    Choose between {minParts} and {maxParts} segments to automatically
                    distribute your audio.
                </p>
            </div>

            <div class="pt-2 space-y-2">
                <button
                    type="submit"
                    class="btn btn-primary w-full flex items-center justify-center gap-2 bg-primary-500 hover:bg-primary-400 border-0"
                    disabled={isLoading}
                >
                    {#if isLoading}
                        <span
                            class="h-4 w-4 border-2 border-surface-50 border-t-transparent rounded-full animate-spin"
                        ></span>
                        <span>Generation currently being processed...</span>
                    {:else}
                        <span>Generate the videos</span>
                    {/if}
                </button>

                {#if isLoading}
                    <p class="text-xs text-center text-surface-100/80">
                        Processing may take up to several minutes depending on
                        the file size.
                    </p>
                {/if}
            </div>

            {#if isLoading}
                <div class="space-y-2 mt-4">
                    <p class="text-xs text-surface-100/80">
                        Processing clips: {currentSegment} / {parts}
                    </p>
                    <div class="space-y-1 max-h-52 overflow-y-auto pr-1">
                        {#each Array(parts) as _, index}
                            {#if index + 1 < currentSegment}
                                <div class="flex items-center gap-2">
                                    <span
                                        class="text-[11px] text-surface-100/80 w-20 shrink-0"
                                    >
                                        Clip {index + 1}
                                    </span>
                                    <div
                                        class="flex-1 h-1.5 rounded-full bg-surface-800 overflow-hidden"
                                    >
                                        <div
                                            class="h-full w-full bg-emerald-400"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-[11px] text-emerald-400 shrink-0"
                                    >
                                        done
                                    </span>
                                </div>
                            {:else if index + 1 === currentSegment}
                                <div class="flex items-center gap-2">
                                    <span
                                        class="text-[11px] text-surface-100/80 w-20 shrink-0"
                                    >
                                        Clip {index + 1}
                                    </span>
                                    <div
                                        class="flex-1 h-1.5 rounded-full bg-surface-800 overflow-hidden"
                                    >
                                        <div
                                            class="h-full w-2/3 bg-primary-400 animate-pulse"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-[11px] text-primary-300 shrink-0"
                                    >
                                        processing…
                                    </span>
                                </div>
                            {:else}
                                <div class="flex items-center gap-2 opacity-60">
                                    <span
                                        class="text-[11px] text-surface-100/80 w-20 shrink-0"
                                    >
                                        Clip {index + 1}
                                    </span>
                                    <div
                                        class="flex-1 h-1.5 rounded-full bg-surface-800 overflow-hidden"
                                    >
                                        <div
                                            class="h-full w-0 bg-primary-400"
                                        ></div>
                                    </div>
                                    <span
                                        class="text-[11px] text-surface-400 shrink-0"
                                    >
                                        pending
                                    </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                </div>
            {/if}
        </form>
    </div>
</section>
