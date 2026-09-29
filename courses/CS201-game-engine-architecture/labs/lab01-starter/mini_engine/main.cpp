// Kiln mini engine: start-up, a three-frame loop, shut-down.
#include <cstdio>
#include "core/log.h"
#include "engine/audio.h"
#include "engine/renderer.h"
#include "game/game.h"
#include "game/save.h"
#include "platform/clock.h"
#include "platform/window.h"

int main() {
    platform_open_window(320, 200);
    core_log("engine started");
    std::printf("save slot 1 exists: %s\n", save_slot_exists(1) ? "yes" : "no");

    for (int frame = 0; frame < 3; ++frame) {
        platform_poll_events();
        entity_step(g_player.body, 1.0f / 60.0f);
        render_sprite(g_player.name, g_player.body.position);
    }
    audio_play("jingle");
    core_log("engine stopped");
    return g_live_allocations == 0 ? 0 : 1;
}
