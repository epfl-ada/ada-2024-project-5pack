function renderPlayerComponent(el) {
    const template = `
        <div class="strategy-container" v-scope>
            <div class="strategy-toggles">
                <label>
                    <input type="checkbox" v-model="strategies.semantic">
                    <span>Semantic</span>
                </label>
                <label>
                    <input type="checkbox" v-model="strategies.topLinks">
                    <span>Top Links</span>
                </label>
                <label>
                    <input type="checkbox" v-model="strategies.hub">
                    <span>Hub</span>
                </label>
                <label>
                    <input type="checkbox" v-model="strategies.backtrack">
                    <span>Backtrack</span>
                </label>
            </div>
            <div class="results">
                <div class="duration">
                    Duration: {{ duration().toFixed(1) }} ±{{ uncertainty().toFixed(1) }} seconds
                    <div class="confidence-interval">95% CI: [{{ (duration() - uncertainty()).toFixed(1) }}, {{ (duration() + uncertainty()).toFixed(1) }}]</div>
                </div>
                <div class="progress-container">
                    <div class="uncertainty-bar"
                         :style="{
                             left: ((duration() - uncertainty() - 120) / (200 - 120) * 100) + '%',
                             width: ((uncertainty() * 2) / (200 - 120) * 100) + '%'
                         }">
                    </div>
                    <div class="estimate-bar"
                         :style="{
                             left: ((duration() - 120) / (200 - 120) * 100) + '%'
                         }">
                    </div>
                </div>
                <div class="scale">
                    <span>120s</span>
                    <span>200s</span>
                </div>
            </div>
            <div class="summary">
                Active strategies: {{ activeStrategies() }}
            </div>
        </div>
    `;

    el.innerHTML = template;
    
    PetiteVue.createApp({
        strategies: {
            semantic: false,
            topLinks: false,
            hub: false,
            backtrack: false
        },
        duration() {
            let duration = 156.146;
            const s = this.strategies;
            if (s.semantic) duration += -20.593;
            if (s.topLinks) duration += -8.146;
            if (s.hub) duration += 2.477;
            if (s.backtrack) duration += 37.394;
            if (s.semantic && s.hub) duration += -1.764;
            if (s.semantic && s.backtrack) duration += -2.428;
            if (s.topLinks && s.hub) duration += -2.985;
            if (s.hub && s.backtrack) duration += -4.058;
            return duration;
        },
        uncertainty() {
            let varianceSum = 1.098 * 1.098;
            const s = this.strategies;
            if (s.semantic) varianceSum += 0.528 * 0.528;
            if (s.topLinks) varianceSum += 0.549 * 0.549;
            if (s.hub) varianceSum += 0.639 * 0.639;
            if (s.backtrack) varianceSum += 0.625 * 0.625;
            if (s.semantic && s.hub) varianceSum += 0.498 * 0.498;
            if (s.semantic && s.backtrack) varianceSum += 0.472 * 0.472;
            if (s.topLinks && s.hub) varianceSum += 0.493 * 0.493;
            if (s.hub && s.backtrack) varianceSum += 0.651 * 0.651;
            return 1.96 * Math.sqrt(varianceSum);
        },
        progressStyle() {
            const percentage = Math.max(0, Math.min(100,
                (this.duration() - 120) / (200 - 120) * 100
            ));
            return { width: `${percentage}%` };
        },
        activeStrategies() {
            return Object.entries(this.strategies)
                .filter(([_, active]) => active)
                .map(([name]) => name)
                .join(', ') || 'None';
        },
        uncertaintyBarStyle() {
            const duration = this.duration();
            const uncertainty = this.uncertainty();
            const left = Math.max(0, Math.min(100,
                ((duration - uncertainty) - 120) / (200 - 120) * 100
            ));
            const width = Math.max(0, Math.min(100,
                (uncertainty * 2) / (200 - 120) * 100
            ));
            return { 
                left: `${left}%`,
                width: `${width}%`
            };
        }
    }).mount(el)
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.__vue-root.player').forEach(renderPlayerComponent)
})