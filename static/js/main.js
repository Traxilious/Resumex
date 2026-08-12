document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const roleSelect = document.getElementById('target-role');
    const customRoleInput = document.getElementById('custom-role-input');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzerForm = document.getElementById('analyzer-form');
    const submitBtn = document.getElementById('submit-btn');
    const fileBadgeContainer = document.getElementById('file-badge-container');

    const uploadSection = document.getElementById('upload-section');
    const loadingOverlay = document.getElementById('loading-overlay');
    const dashboardSection = document.getElementById('dashboard-section');
    const resetBtn = document.getElementById('reset-btn');

    const historyModal = document.getElementById('history-modal');
    const openHistoryBtn = document.getElementById('open-history-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const historyTableContainer = document.getElementById('history-table-container');

    let scoreChartInstance = null;
    let selectedFile = null;

    // 0. Initialize 60fps Animated Dot Grid Background
    initAnimatedDotGrid();

    // 1. Fetch available target job roles
    fetchRoles();

    function fetchRoles() {
        fetch('/api/roles')
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success' && data.roles) {
                    roleSelect.innerHTML = '';

                    // Separate standard roles and "Other" role
                    const standardRoles = data.roles.filter(r => !r.role_title.startsWith('Other'));
                    const otherRole = data.roles.find(r => r.role_title.startsWith('Other'));

                    standardRoles.forEach((role, idx) => {
                        const opt = document.createElement('option');
                        opt.value = role.role_title;
                        opt.textContent = `${role.role_title} (${role.category})`;
                        if (idx === 0) opt.selected = true;
                        roleSelect.appendChild(opt);
                    });

                    if (otherRole) {
                        const opt = document.createElement('option');
                        opt.value = otherRole.role_title;
                        opt.textContent = `✨ ${otherRole.role_title} (${otherRole.category})`;
                        roleSelect.appendChild(opt);
                    }
                }
            })
            .catch(err => {
                console.error('Error loading roles:', err);
                roleSelect.innerHTML = '<option value="Web Developer">Web Developer (Software Engineering)</option>';
            });
    }

    // Toggle custom role input when "Other" option is selected
    roleSelect.addEventListener('change', () => {
        if (roleSelect.value.startsWith('Other')) {
            customRoleInput.style.display = 'block';
            customRoleInput.focus();
        } else {
            customRoleInput.style.display = 'none';
        }
    });

    // 2. Drag & Drop handling
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, () => dropZone.classList.remove('dragover'));
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        const allowed = ['pdf', 'docx', 'doc', 'txt'];
        const ext = file.name.split('.').pop().toLowerCase();
        if (!allowed.includes(ext)) {
            alert('Unsupported file format! Please upload a PDF, DOCX, or TXT file.');
            return;
        }
        selectedFile = file;
        fileBadgeContainer.innerHTML = `
            <div class="selected-file-badge">
                <i class="fa-solid fa-file-contract"></i> ${file.name} (${(file.size / 1024).toFixed(1)} KB)
            </div>
        `;
    }

    // 3. Submit & Analyze
    analyzerForm.addEventListener('submit', (e) => {
        e.preventDefault();

        if (!selectedFile && fileInput.files.length > 0) {
            selectedFile = fileInput.files[0];
        }

        if (!selectedFile) {
            alert('Please select or drop a resume file first!');
            return;
        }

        let targetRole = roleSelect.value;
        if (targetRole.startsWith('Other') && customRoleInput.value.trim() !== '') {
            targetRole = customRoleInput.value.trim();
        }

        const formData = new FormData();
        formData.append('resume_file', selectedFile);
        formData.append('target_role', targetRole);

        // Show loading state
        uploadSection.style.display = 'none';
        loadingOverlay.style.display = 'block';

        fetch('/api/analyze', {
            method: 'POST',
            body: formData
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(errData => {
                    throw new Error(errData.message || `Server error (${res.status})`);
                }).catch(() => {
                    throw new Error(`Server response error (${res.status})`);
                });
            }
            return res.json();
        })
        .then(data => {
            loadingOverlay.style.display = 'none';
            if (data.status === 'success') {
                renderDashboard(data);
            } else {
                alert('Analysis Error: ' + (data.message || 'Unknown error'));
                uploadSection.style.display = 'block';
            }
        })
        .catch(err => {
            loadingOverlay.style.display = 'none';
            uploadSection.style.display = 'block';
            if (err.message && err.message.includes('Failed to fetch')) {
                alert('Server Connection Notice: Free cloud hosting server is waking up (cold start). Please wait 10-15 seconds and click "Run Deep Analysis" again!');
            } else {
                alert('Notice: ' + err.message);
            }
        });
    });

    // 4. Render Dashboard View
    function renderDashboard(data) {
        dashboardSection.style.display = 'block';

        // Header info
        document.getElementById('res-target-role').textContent = data.target_role;
        document.getElementById('res-filename').textContent = data.filename;

        // Executive Verdict Banner
        if (data.verdict) {
            document.getElementById('verdict-status').textContent = data.verdict.status;
            const iconBox = document.getElementById('verdict-icon-box');
            const iconElem = document.getElementById('verdict-icon');

            iconBox.className = `verdict-icon-box ${data.verdict.badge_color}`;
            iconElem.className = `fa-solid ${data.verdict.icon}`;

            document.getElementById('banner-overall-score').textContent = `${data.overall_score}/100`;
            document.getElementById('banner-ats-score').textContent = `${data.ats_score}%`;
            document.getElementById('banner-authenticity-score').textContent = `${data.ai_score}%`;
        }

        // Animated Scores
        animateValue('res-overall-score', 0, data.overall_score, 1000);
        animateValue('res-ats-score', 0, data.ats_score, 1000, '%');
        animateValue('res-authenticity-score', 0, data.ai_score, 1000, '%');

        // Authenticity Risk Tag styling
        const authenticityRiskTag = document.getElementById('authenticity-risk-tag');
        const resAuthenticityScore = document.getElementById('res-authenticity-score');
        if (data.ai_details) {
            authenticityRiskTag.textContent = data.ai_details.risk_level;
            const colorClass = data.ai_details.color === 'emerald' ? 'text-emerald' : (data.ai_details.color === 'rose' ? 'text-rose' : 'text-amber');
            authenticityRiskTag.className = colorClass;

            if (data.ai_details.color === 'emerald') {
                resAuthenticityScore.style.color = 'var(--accent-emerald)';
            } else if (data.ai_details.color === 'rose') {
                resAuthenticityScore.style.color = 'var(--accent-rose)';
            } else {
                resAuthenticityScore.style.color = 'var(--accent-amber)';
            }
        }

        // Ratio & Stats
        document.getElementById('ats-matched-ratio').textContent = 
            `${data.ats_details.total_matched} Matched Skills Identified`;

        const parsed = data.parsed_info;
        document.getElementById('res-word-count').textContent = `${parsed.word_count} words`;

        const contact = parsed.contact_info;

        // Email
        document.getElementById('res-email-found').innerHTML = contact.email 
            ? `<span style="color: var(--accent-emerald); max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: bottom;" title="${contact.email}"><i class="fa-solid fa-check-circle"></i> ${contact.email}</span>` 
            : `<span style="color: var(--accent-rose);"><i class="fa-solid fa-times-circle"></i> Missing</span>`;

        // Phone Number
        document.getElementById('res-phone-found').innerHTML = contact.phone 
            ? `<span style="color: var(--accent-emerald); max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: bottom;" title="${contact.phone}"><i class="fa-solid fa-check-circle"></i> ${contact.phone}</span>` 
            : `<span style="color: var(--accent-rose);"><i class="fa-solid fa-times-circle"></i> Missing</span>`;

        // LinkedIn
        document.getElementById('res-linkedin-found').innerHTML = contact.linkedin 
            ? `<span style="color: var(--accent-emerald); max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: bottom;" title="${contact.linkedin}"><i class="fa-solid fa-check-circle"></i> Found</span>` 
            : `<span style="color: var(--accent-rose);"><i class="fa-solid fa-times-circle"></i> Missing</span>`;

        // GitHub
        document.getElementById('res-github-found').innerHTML = (contact.github || contact.portfolio) 
            ? `<span style="color: var(--accent-emerald); max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: bottom;" title="${contact.github || contact.portfolio}"><i class="fa-solid fa-check-circle"></i> Found</span>` 
            : `<span style="color: var(--accent-rose);"><i class="fa-solid fa-times-circle"></i> Missing</span>`;

        // Render PROS List
        const prosList = document.getElementById('pros-list');
        prosList.innerHTML = '';
        if (data.pros && data.pros.length > 0) {
            data.pros.forEach(p => {
                const li = document.createElement('li');
                li.textContent = p;
                prosList.appendChild(li);
            });
        } else {
            prosList.innerHTML = '<li>Basic text formatting detected.</li>';
        }

        // Render CONS List
        const consList = document.getElementById('cons-list');
        consList.innerHTML = '';
        if (data.cons && data.cons.length > 0) {
            data.cons.forEach(c => {
                const li = document.createElement('li');
                li.textContent = c;
                consList.appendChild(li);
            });
        } else {
            consList.innerHTML = '<li>No major critical vulnerabilities found.</li>';
        }

        // Skill Badges
        const matchedContainer = document.getElementById('matched-skills-container');
        const missingContainer = document.getElementById('missing-skills-container');
        matchedContainer.innerHTML = '';
        missingContainer.innerHTML = '';

        if (data.ats_details.matched_skills.length === 0) {
            matchedContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 0.9rem;">No direct matching keywords found.</span>';
        } else {
            data.ats_details.matched_skills.forEach(skill => {
                const badge = document.createElement('span');
                badge.className = 'badge badge-matched';
                badge.innerHTML = `<i class="fa-solid fa-check"></i> ${capitalize(skill)}`;
                matchedContainer.appendChild(badge);
            });
        }

        const allMissing = [...data.ats_details.missing_core, ...data.ats_details.missing_optional];
        if (allMissing.length === 0) {
            missingContainer.innerHTML = '<span style="color: var(--accent-emerald); font-size: 0.9rem;">Great job! All target keywords matched.</span>';
        } else {
            allMissing.forEach(skill => {
                const badge = document.createElement('span');
                badge.className = 'badge badge-missing';
                badge.innerHTML = `<i class="fa-solid fa-plus"></i> ${capitalize(skill)}`;
                missingContainer.appendChild(badge);
            });
        }

        // Render Chart.js Breakdown Chart
        renderScoreChart(data.score_breakdown);

        // Render Suggestions Cards
        const sugList = document.getElementById('suggestions-list');
        sugList.innerHTML = '';

        if (!data.feedback || data.feedback.length === 0) {
            sugList.innerHTML = '<div style="color: var(--accent-emerald);">No critical issues found! Your resume aligns well with target expectations.</div>';
        } else {
            data.feedback.forEach(sug => {
                const prioLower = sug.priority.toLowerCase();
                const card = document.createElement('div');
                card.className = `suggestion-card ${prioLower}`;
                card.innerHTML = `
                    <div class="sug-header">
                        <div class="sug-title">${sug.title}</div>
                        <span class="prio-tag prio-${prioLower}">${sug.priority} Priority</span>
                    </div>
                    <div class="sug-desc">${sug.description}</div>
                    <div class="sug-action"><i class="fa-solid fa-arrow-right-long"></i> Action: ${sug.action}</div>
                `;
                sugList.appendChild(card);
            });
        }

        // Render Recommended Portfolio Projects
        const projectsContainer = document.getElementById('recommended-projects-container');
        projectsContainer.innerHTML = '';

        if (data.learning_roadmap && data.learning_roadmap.projects && data.learning_roadmap.projects.length > 0) {
            data.learning_roadmap.projects.forEach(p => {
                const pCard = document.createElement('div');
                pCard.className = 'project-card';
                
                const stackBadges = p.tech_stack 
                    ? p.tech_stack.map(tech => `<span class="badge badge-matched" style="font-size: 0.7rem; padding: 0.15rem 0.45rem;">${tech}</span>`).join(' ')
                    : '';

                pCard.innerHTML = `
                    <div class="proj-header">
                        <div class="proj-title"><i class="fa-solid fa-cube" style="color: var(--accent-cyan);"></i> ${p.title}</div>
                        <span class="proj-diff">${p.difficulty}</span>
                    </div>
                    <div class="proj-desc">${p.description}</div>
                    <div style="margin-bottom: 0.6rem; display: flex; flex-wrap: wrap; gap: 4px;">${stackBadges}</div>
                    <div class="proj-impact"><i class="fa-solid fa-chart-line"></i> Impact: ${p.resume_impact}</div>
                `;
                projectsContainer.appendChild(pCard);
            });
        } else {
            projectsContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;">No additional project recommendations required.</div>';
        }

        // Render Curated Learning Resources
        const resourcesContainer = document.getElementById('curated-resources-container');
        resourcesContainer.innerHTML = '';

        if (data.learning_roadmap && data.learning_roadmap.resources && data.learning_roadmap.resources.length > 0) {
            data.learning_roadmap.resources.forEach(r => {
                const rRow = document.createElement('a');
                rRow.className = 'resource-row';
                rRow.href = r.url;
                rRow.target = '_blank';
                rRow.rel = 'noopener noreferrer';
                
                const isYoutube = r.type.includes('YouTube') || r.url.includes('youtube');

                rRow.innerHTML = `
                    <div>
                        <div class="res-title-link">
                            <i class="${isYoutube ? 'fa-brands fa-youtube' : 'fa-solid fa-book-open'}" style="color: ${isYoutube ? '#ff0000' : 'var(--accent-emerald)'};"></i>
                            ${r.title} <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 0.75rem; color: var(--accent-cyan); margin-left: 4px;"></i>
                        </div>
                        <div class="res-desc">${r.description}</div>
                    </div>
                    <div class="res-type-badge">
                        ${r.source} (${r.type})
                    </div>
                `;
                resourcesContainer.appendChild(rRow);
            });
        } else {
            resourcesContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;">No additional learning resources required.</div>';
        }

        // Render Big Executive Summary Narrative
        const summaryElem = document.getElementById('executive-summary-text');
        if (data.executive_summary) {
            const paragraphs = data.executive_summary.split('\n\n');
            summaryElem.innerHTML = paragraphs.map(p => `<p>${p}</p>`).join('');
        } else {
            summaryElem.innerHTML = '<p>Evaluation complete. Review the Pros, Cons, and Action Plan above for specific optimizations.</p>';
        }
    }

    // Chart.js Visualization
    function renderScoreChart(breakdown) {
        const ctx = document.getElementById('scoreChart').getContext('2d');
        
        if (scoreChartInstance) {
            scoreChartInstance.destroy();
        }

        const labels = ['Section Completeness', 'Contact Details', 'Resume Length', 'Action & Impact', 'Skill Alignment'];
        const scores = [
            breakdown.section_completeness.score,
            breakdown.contact_details.score,
            breakdown.resume_length.score,
            breakdown.action_impact.score,
            breakdown.skill_relevancy.score
        ];
        const maxes = [30, 15, 15, 20, 20];

        scoreChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Achieved Points',
                        data: scores,
                        backgroundColor: 'rgba(15, 23, 42, 0.85)',
                        borderColor: '#0f172a',
                        borderWidth: 1,
                        borderRadius: 4
                    },
                    {
                        label: 'Max Possible',
                        data: maxes,
                        backgroundColor: 'rgba(226, 232, 240, 0.6)',
                        borderColor: '#cbd5e1',
                        borderWidth: 1,
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#475569', font: { family: 'Plus Jakarta Sans' } }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#64748b' },
                        grid: { color: 'rgba(226, 232, 240, 0.6)' }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#64748b' },
                        grid: { color: 'rgba(226, 232, 240, 0.6)' }
                    }
                }
            }
        });
    }

    // Reset button
    resetBtn.addEventListener('click', () => {
        dashboardSection.style.display = 'none';
        uploadSection.style.display = 'block';
        selectedFile = null;
        fileInput.value = '';
        fileBadgeContainer.innerHTML = '';
        customRoleInput.style.display = 'none';
        customRoleInput.value = '';
    });

    // History Modal logic
    openHistoryBtn.addEventListener('click', () => {
        historyModal.style.display = 'flex';
        fetch('/api/history')
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success' && data.history) {
                    if (data.history.length === 0) {
                        historyTableContainer.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No past evaluations recorded yet.</p>';
                    } else {
                        let html = `
                            <table class="history-table">
                                <thead>
                                    <tr>
                                        <th>File</th>
                                        <th>Target Role</th>
                                        <th>Score</th>
                                        <th>ATS Score</th>
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                        `;
                        data.history.forEach(item => {
                            html += `
                                <tr>
                                    <td><i class="fa-solid fa-file-lines" style="color: #0f172a;"></i> ${item.filename}</td>
                                    <td>${item.target_role}</td>
                                    <td><strong style="color: #059669;">${item.overall_score}/100</strong></td>
                                    <td><strong style="color: #0891b2;">${item.ats_score}%</strong></td>
                                    <td style="color: var(--text-muted); font-size: 0.8rem;">${new Date(item.analyzed_at).toLocaleDateString()}</td>
                                </tr>
                            `;
                        });
                        html += '</tbody></table>';
                        historyTableContainer.innerHTML = html;
                    }
                }
            });
    });

    closeModalBtn.addEventListener('click', () => historyModal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === historyModal) historyModal.style.display = 'none';
    });

    // 5. 60fps Random Growing & Shrinking Dot Grid Canvas Animation
    function initAnimatedDotGrid() {
        const canvas = document.getElementById('dot-grid-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const spacing = 28;
        const dots = [];

        function buildGrid() {
            dots.length = 0;
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;

            const cols = Math.ceil(width / spacing) + 1;
            const rows = Math.ceil(height / spacing) + 1;

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    dots.push({
                        x: c * spacing,
                        y: r * spacing,
                        baseRadius: 1.0,
                        maxRadius: 2.8,
                        pulseSpeed: 0.01 + Math.random() * 0.02,
                        pulsePhase: Math.random() * Math.PI * 2,
                        alphaBase: 0.12 + Math.random() * 0.12
                    });
                }
            }
        }

        buildGrid();
        window.addEventListener('resize', buildGrid);

        function animate() {
            ctx.clearRect(0, 0, width, height);

            for (let i = 0; i < dots.length; i++) {
                const d = dots[i];
                d.pulsePhase += d.pulseSpeed;

                const factor = (Math.sin(d.pulsePhase) + 1) / 2;
                const radius = d.baseRadius + (d.maxRadius - d.baseRadius) * factor;
                const alpha = d.alphaBase + factor * 0.25;

                ctx.beginPath();
                ctx.arc(d.x, d.y, radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(148, 163, 184, ${alpha})`;
                ctx.fill();
            }

            requestAnimationFrame(animate);
        }

        animate();
    }

    // Helpers
    function animateValue(id, start, end, duration, suffix = '') {
        const obj = document.getElementById(id);
        if (!obj) return;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start) + suffix;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
});
