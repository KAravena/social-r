#!/usr/bin/env python3
"""
Social R — Administrator Authorization & Free Navigation QA Test Suite
Validates:
A. ADMIN Katherine: can open M13 directly.
B. ADMIN Juan Carlos: can open challenge M13 directly.
C. ADMIN Tomás: can jump M01 -> M08 -> M13.
D. ADMIN Gabriel: can jump M01 -> M10 -> challenge M13.
E. Regular student: cannot bypass gating.
F. Guest: maintains default pedagogical gating.
G. Admin logout -> regular student login: admin state removed and gating restored.
H. Admin challenge direct access: opens challenge without auto-completing or auto-passing.
I. Security: client-side privilege escalation prevented.
J. Roster importer & progress exporter role handling.

IMPORTANT: Strictly uses synthetic identifiers, mock sessions, and synthetic UUIDs.
Zero real RUTs are included.
"""

import asyncio
import http.server
import json
import os
import re
import socket
import sys
import threading
import unittest
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.rut_utils import validate_rut, normalize_rut, format_rut_masked, clean_rut


class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "docs"), **kwargs)

    def log_message(self, format, *args):
        pass


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class AdminFreeNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", cls.port), DocsHTTPHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_async(self, coro):
        return asyncio.run(coro)

    # --------------------------------------------------------------------------
    # A. ADMIN Katherine: can open M13 directly
    # --------------------------------------------------------------------------
    def test_case_a_admin_katherine_can_open_m13_directly(self):
        """Case A: Admin Katherine can open M13 directly without completing prior modules."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !config || !nav) return { ok: false, error: 'globals missing' };

                    // Synthetic admin session for Katherine
                    cloud.setSession({
                        sessionToken: 'synth_tok_kath_001',
                        student: {
                            id: '00000000-0000-4000-8000-000000000001',
                            displayName: 'Katherine Aravena',
                            rutMasked: '••.•••.198-9',
                            section: 'TEST-ADMIN',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    // Evaluate module unlocking and exercise unlocking for M13
                    const m13Unlocked = config.isModuleUnlocked('13-de-la-pregunta-al-analisis');
                    const m13ExUnlocked = config.isExerciseUnlocked({ id: 'intro-r-13-001', moduleId: '13-de-la-pregunta-al-analisis', order: 0 });

                    // Find index of intro-r-13-001 and set active
                    const ex13Idx = nav.exercises.findIndex(e => e.id === 'intro-r-13-001');
                    nav.setActiveIndex(ex13Idx);
                    const currentEx = nav.getCurrentExercise();

                    return {
                        ok: true,
                        isAdmin: cloud.isAdmin(),
                        role: cloud.getRole(),
                        m13Unlocked,
                        m13ExUnlocked,
                        currentExId: currentEx ? currentEx.id : null,
                        currentIndex: nav.currentIndex
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["isAdmin"], "Session must have isAdmin=True")
        self.assertEqual(data["role"], "admin", "Session must have role=admin")
        self.assertTrue(data["m13Unlocked"], "Admin must have M13 unlocked")
        self.assertTrue(data["m13ExUnlocked"], "Admin must have intro-r-13-001 unlocked")
        self.assertEqual(data["currentExId"], "intro-r-13-001", "Admin must successfully activate intro-r-13-001")

    # --------------------------------------------------------------------------
    # B. ADMIN Juan Carlos: can open challenge M13 directly
    # --------------------------------------------------------------------------
    def test_case_b_admin_juan_carlos_can_open_challenge_m13_directly(self):
        """Case B: Admin Juan Carlos can open final challenge of M13 directly."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    const store = window.SocialR && window.SocialR.progress;
                    if (!cloud || !config || !nav) return { ok: false };

                    // Synthetic admin session for Juan Carlos
                    cloud.setSession({
                        sessionToken: 'synth_tok_jc_002',
                        student: {
                            id: '00000000-0000-4000-8000-000000000002',
                            displayName: 'Juan Carlos Castillo Valenzuela',
                            rutMasked: '••.•••.714-K',
                            section: 'TEST-ADMIN',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    const chM13Unlocked = config.isChallengeUnlocked('13-de-la-pregunta-al-analisis');
                    nav.setActiveChallengeById('intro-r-13-challenge');

                    const isViewing = nav.isViewingChallenge;
                    const activeChId = nav.activeChallenge ? nav.activeChallenge.id : null;
                    const isPassedBefore = store ? store.isChallengePassed('13-de-la-pregunta-al-analisis') : null;

                    return {
                        ok: true,
                        isAdmin: cloud.isAdmin(),
                        chM13Unlocked,
                        isViewing,
                        activeChId,
                        isPassedBefore
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["isAdmin"], "Admin privilege must be verified")
        self.assertTrue(data["chM13Unlocked"], "Challenge M13 must be unlocked for admin")
        self.assertTrue(data["isViewing"], "Navigation must be in viewing challenge mode")
        self.assertEqual(data["activeChId"], "intro-r-13-challenge", "Active challenge must be intro-r-13-challenge")
        self.assertFalse(data["isPassedBefore"], "Challenge must NOT be automatically marked as passed")

    # --------------------------------------------------------------------------
    # C. ADMIN Tomás: can jump M01 -> M08 -> M13
    # --------------------------------------------------------------------------
    def test_case_c_admin_tomas_can_jump_m01_m08_m13(self):
        """Case C: Admin Tomás can jump arbitrarily from M01 to M08 to M13."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !nav) return { ok: false };

                    // Synthetic admin session for Tomás
                    cloud.setSession({
                        sessionToken: 'synth_tok_tomas_003',
                        student: {
                            id: '00000000-0000-4000-8000-000000000003',
                            displayName: 'Tomás Ignacio Urzúa Moreno',
                            rutMasked: '••.•••.496-2',
                            section: 'TEST-ADMIN',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    // Jump to M01
                    const idx1 = nav.exercises.findIndex(e => e.id === 'intro-r-01-001');
                    nav.setActiveIndex(idx1);
                    const pos1 = nav.getCurrentExercise().id;

                    // Jump to M08
                    const idx8 = nav.exercises.findIndex(e => e.id === 'intro-r-08-001');
                    nav.setActiveIndex(idx8);
                    const pos8 = nav.getCurrentExercise().id;

                    // Jump to M13
                    const idx13 = nav.exercises.findIndex(e => e.id === 'intro-r-13-001');
                    nav.setActiveIndex(idx13);
                    const pos13 = nav.getCurrentExercise().id;

                    return {
                        ok: true,
                        isAdmin: cloud.isAdmin(),
                        pos1,
                        pos8,
                        pos13
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["isAdmin"])
        self.assertEqual(data["pos1"], "intro-r-01-001")
        self.assertEqual(data["pos8"], "intro-r-08-001")
        self.assertEqual(data["pos13"], "intro-r-13-001")

    # --------------------------------------------------------------------------
    # D. ADMIN Gabriel: can jump M01 -> M10 -> challenge M13
    # --------------------------------------------------------------------------
    def test_case_d_admin_gabriel_can_jump_m01_m10_challenge_m13(self):
        """Case D: Admin Gabriel can jump M01 -> M10 -> challenge M13."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !nav) return { ok: false };

                    // Synthetic admin session for Gabriel
                    cloud.setSession({
                        sessionToken: 'synth_tok_gabriel_004',
                        student: {
                            id: '00000000-0000-4000-8000-000000000004',
                            displayName: 'Gabriel Nicolás Cortés Paredes',
                            rutMasked: '••.•••.962-5',
                            section: 'TEST-ADMIN',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    // Jump to M10
                    const idx10 = nav.exercises.findIndex(e => e.id === 'intro-r-10-001');
                    nav.setActiveIndex(idx10);
                    const pos10 = nav.getCurrentExercise().id;

                    // Jump to Challenge M13
                    nav.setActiveChallengeById('intro-r-13-challenge');
                    const isViewing = nav.isViewingChallenge;
                    const activeChId = nav.activeChallenge ? nav.activeChallenge.id : null;

                    return {
                        ok: true,
                        isAdmin: cloud.isAdmin(),
                        pos10,
                        isViewing,
                        activeChId
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["isAdmin"])
        self.assertEqual(data["pos10"], "intro-r-10-001")
        self.assertTrue(data["isViewing"])
        self.assertEqual(data["activeChId"], "intro-r-13-challenge")

    # --------------------------------------------------------------------------
    # E. Regular student: cannot bypass gating
    # --------------------------------------------------------------------------
    def test_case_e_regular_student_cannot_bypass_gating(self):
        """Case E: Regular student cannot bypass pedagogical gating."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !config || !nav) return { ok: false };

                    // Synthetic regular student session
                    cloud.setSession({
                        sessionToken: 'synth_tok_student_001',
                        student: {
                            id: '00000000-0000-4000-8000-000000000099',
                            displayName: 'Estudiante Normal',
                            rutMasked: '••.•••.123-4',
                            section: '1',
                            role: 'student',
                            isAdmin: false
                        }
                    });

                    // Module M02 should be locked without M01 completion
                    const m02Unlocked = config.isModuleUnlocked('02-trabajar-con-varios-valores');
                    // Module M13 should be locked
                    const m13Unlocked = config.isModuleUnlocked('13-de-la-pregunta-al-analisis');
                    // Challenge M13 should be locked
                    const ch13Unlocked = config.isChallengeUnlocked('13-de-la-pregunta-al-analisis');

                    // Attempting to jump to M13 via setActiveIndex must be blocked
                    const idx13 = nav.exercises.findIndex(e => e.id === 'intro-r-13-001');
                    nav.setActiveIndex(0); // start at M01-E01
                    nav.setActiveIndex(idx13); // try jump to M13
                    const currentAfterAttempt = nav.getCurrentExercise().id;

                    return {
                        ok: true,
                        isAdmin: cloud.isAdmin(),
                        role: cloud.getRole(),
                        m02Unlocked,
                        m13Unlocked,
                        ch13Unlocked,
                        currentAfterAttempt
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertFalse(data["isAdmin"], "Regular student must not be admin")
        self.assertEqual(data["role"], "student")
        self.assertFalse(data["m02Unlocked"], "M02 must be locked for regular student with 0 progress")
        self.assertFalse(data["m13Unlocked"], "M13 must be locked for regular student")
        self.assertFalse(data["ch13Unlocked"], "Challenge M13 must be locked for regular student")
        self.assertEqual(data["currentAfterAttempt"], "intro-r-01-001", "Attempt to activate M13 must be blocked")

    # --------------------------------------------------------------------------
    # F. Guest: maintains default pedagogical gating
    # --------------------------------------------------------------------------
    def test_case_f_guest_mode_preserved(self):
        """Case F: Guest mode preserves existing pedagogical gating rules."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !config || !nav) return { ok: false };

                    // Clear session and enable guest mode
                    cloud.clearSession();
                    cloud.setGuestMode(true);

                    const isAuth = cloud.isAuthenticated();
                    const isAdmin = cloud.isAdmin();
                    const isGuest = cloud.isGuestMode();

                    const m01Unlocked = config.isModuleUnlocked('01-empezar-a-pensar-con-r');
                    const m02Unlocked = config.isModuleUnlocked('02-trabajar-con-varios-valores');
                    const m13Unlocked = config.isModuleUnlocked('13-de-la-pregunta-al-analisis');

                    return {
                        ok: true,
                        isAuth,
                        isAdmin,
                        isGuest,
                        m01Unlocked,
                        m02Unlocked,
                        m13Unlocked
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertFalse(data["isAuth"])
        self.assertFalse(data["isAdmin"])
        self.assertTrue(data["isGuest"])
        self.assertTrue(data["m01Unlocked"], "M01 must be unlocked for guest")
        self.assertFalse(data["m02Unlocked"], "M02 must be locked for guest with 0 progress")
        self.assertFalse(data["m13Unlocked"], "M13 must be locked for guest")

    # --------------------------------------------------------------------------
    # G. Admin logout -> regular student login: admin state removed
    # --------------------------------------------------------------------------
    def test_case_g_admin_logout_then_regular_login(self):
        """Case G: Logging out of admin and logging in as regular student completely strips admin privileges."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    if (!cloud || !config) return { ok: false };

                    // 1. Admin login
                    cloud.setSession({
                        sessionToken: 'synth_admin_session',
                        student: {
                            id: '00000000-0000-4000-8000-000000000001',
                            displayName: 'Katherine Aravena',
                            role: 'admin',
                            isAdmin: true
                        }
                    });
                    const step1_isAdmin = cloud.isAdmin();
                    const step1_m13Unlocked = config.isModuleUnlocked('13-de-la-pregunta-al-analisis');

                    // 2. Admin logout
                    cloud.clearSession();
                    const step2_isAdmin = cloud.isAdmin();
                    const step2_isAuth = cloud.isAuthenticated();

                    // 3. Regular student login
                    cloud.setSession({
                        sessionToken: 'synth_student_session',
                        student: {
                            id: '00000000-0000-4000-8000-000000000099',
                            displayName: 'Estudiante Regular',
                            role: 'student',
                            isAdmin: false
                        }
                    });
                    const step3_isAdmin = cloud.isAdmin();
                    const step3_m13Unlocked = config.isModuleUnlocked('13-de-la-pregunta-al-analisis');

                    return {
                        ok: true,
                        step1_isAdmin,
                        step1_m13Unlocked,
                        step2_isAdmin,
                        step2_isAuth,
                        step3_isAdmin,
                        step3_m13Unlocked
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        # Step 1: Admin
        self.assertTrue(data["step1_isAdmin"])
        self.assertTrue(data["step1_m13Unlocked"])
        # Step 2: Logout
        self.assertFalse(data["step2_isAdmin"])
        self.assertFalse(data["step2_isAuth"])
        # Step 3: Regular student
        self.assertFalse(data["step3_isAdmin"])
        self.assertFalse(data["step3_m13Unlocked"], "Regular student must not have M13 unlocked")

    # --------------------------------------------------------------------------
    # H. Admin challenge direct access: opens without auto-completing
    # --------------------------------------------------------------------------
    def test_case_h_admin_challenge_direct_access_does_not_auto_pass(self):
        """Case H: Admin can access challenge directly, but challenge is NOT auto-passed or auto-completed."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    const store = window.SocialR && window.SocialR.progress;
                    if (!cloud || !nav || !store) return { ok: false };

                    // Admin login
                    cloud.setSession({
                        sessionToken: 'synth_admin_session',
                        student: {
                            id: '00000000-0000-4000-8000-000000000001',
                            displayName: 'Katherine Aravena',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    // Direct challenge navigation
                    nav.setActiveChallengeById('intro-r-13-challenge');

                    const isViewing = nav.isViewingChallenge;
                    const isPassed = store.isChallengePassed('13-de-la-pregunta-al-analisis');
                    const chStatus = store.getChallengeStatus ? store.getChallengeStatus('13-de-la-pregunta-al-analisis') : (store.state.challenges['13-de-la-pregunta-al-analisis'] ? store.state.challenges['13-de-la-pregunta-al-analisis'].status : null);

                    const completedExercises = store.state.modules['13-de-la-pregunta-al-analisis'] ? store.state.modules['13-de-la-pregunta-al-analisis'].completedExercises : [];

                    return {
                        ok: true,
                        isViewing,
                        isPassed,
                        chStatus,
                        completedCount: completedExercises.length
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["isViewing"], "Must open challenge view")
        self.assertFalse(data["isPassed"], "Challenge must NOT be marked passed on entry")
        self.assertNotEqual(data["chStatus"], "passed", "Challenge status must NOT be 'passed'")
        self.assertEqual(data["completedCount"], 0, "No exercises must be auto-completed")

    # --------------------------------------------------------------------------
    # I. Security: Client-side privilege escalation prevented
    # --------------------------------------------------------------------------
    def test_case_i_client_side_tampering_reconciliation(self):
        """Case I: Client-side role tampering is overwritten when verified with server data."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const adapter = window.SocialR && window.SocialR.cloudAdapter;
                    if (!cloud || !adapter) return { ok: false };

                    // 1. Attacker maliciously sets isAdmin: true in localStorage for a regular student session
                    const tamperedSession = {
                        sessionToken: 'synth_tampered_token',
                        student: {
                            id: '00000000-0000-4000-8000-000000000099',
                            displayName: 'Estudiante Malicioso',
                            role: 'admin',
                            isAdmin: true
                        }
                    };
                    localStorage.setItem(cloud.sessionStorageKey, JSON.stringify(tamperedSession));

                    // 2. Mock window.fetch so fetchCloudProgress executes its actual reconciliation logic
                    const origFetch = window.fetch;
                    window.fetch = async (url, opts) => {
                        if (typeof url === 'string' && url.includes('student-progress-get')) {
                            return {
                                ok: true,
                                status: 200,
                                json: async () => ({
                                    completedExercises: [],
                                    challenges: {},
                                    editorState: {},
                                    student: {
                                        role: 'student',
                                        isAdmin: false,
                                        section: '1'
                                    }
                                })
                            };
                        }
                        return origFetch(url, opts);
                    };

                    // Reconcile progress via fetchCloudProgress
                    const data = await adapter.fetchCloudProgress();
                    window.fetch = origFetch;

                    // Check if session was overwritten/demoted
                    const currentSession = cloud.getSession();

                    return {
                        ok: true,
                        clientTamperedBefore: tamperedSession.student.isAdmin,
                        sessionRoleAfter: currentSession.student.role,
                        sessionIsAdminAfter: currentSession.student.isAdmin
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertTrue(data["clientTamperedBefore"])
        # Server authoritative data must have stripped the admin role
        self.assertEqual(data["sessionRoleAfter"], "student")
        self.assertFalse(data["sessionIsAdminAfter"])

    # --------------------------------------------------------------------------
    # J. Previous / Next unrestricted navigation for admin
    # --------------------------------------------------------------------------
    def test_case_j_admin_prev_next_unrestricted(self):
        """Case J: Admin has unrestricted Previous and Next buttons across modules."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                res = await page.evaluate("""async () => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const nav = window.SocialR && window.SocialR.navigation;
                    if (!cloud || !nav) return { ok: false };

                    // Admin login
                    cloud.setSession({
                        sessionToken: 'synth_admin_session',
                        student: {
                            id: '00000000-0000-4000-8000-000000000001',
                            displayName: 'Katherine Aravena',
                            role: 'admin',
                            isAdmin: true
                        }
                    });

                    // Jump to last exercise of M01 (intro-r-01-008)
                    const ex8Idx = nav.exercises.findIndex(e => e.id === 'intro-r-01-008');
                    nav.setActiveIndex(ex8Idx);
                    nav.refreshUI();

                    const nextBtn = document.getElementById('sr-btn-next');
                    const nextDisabled = nextBtn ? nextBtn.disabled : true;

                    // Click next -> opens challenge
                    nav.next();
                    const isViewingCh = nav.isViewingChallenge;
                    const chModId = nav.activeChallenge ? nav.activeChallenge.moduleId : null;

                    // From challenge, next is also available for admin to jump to M02
                    nav.refreshUIForChallenge(nav.activeChallenge);
                    const chNextDisabled = nextBtn ? nextBtn.disabled : true;

                    // Click next from challenge -> goes to M02-E01
                    nav.next();
                    const curExAfterChNext = nav.getCurrentExercise() ? nav.getCurrentExercise().id : null;

                    // From M02-E01, Previous button is enabled for admin to go back
                    const prevBtn = document.getElementById('sr-btn-prev');
                    nav.refreshUI();
                    const prevDisabled = prevBtn ? prevBtn.disabled : true;

                    nav.previous();
                    const curExAfterPrev = nav.getCurrentExercise() ? nav.getCurrentExercise().id : null;

                    return {
                        ok: true,
                        nextDisabled,
                        isViewingCh,
                        chModId,
                        chNextDisabled,
                        curExAfterChNext,
                        prevDisabled,
                        curExAfterPrev
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"), f"Evaluation failed: {data}")
        self.assertFalse(data["nextDisabled"], "Next button must be enabled on last exercise for admin")
        self.assertTrue(data["isViewingCh"], "Next from last exercise must open challenge")
        self.assertEqual(data["chModId"], "01-empezar-a-pensar-con-r")
        self.assertFalse(data["chNextDisabled"], "Next button on challenge must be enabled for admin")
        self.assertEqual(data["curExAfterChNext"], "intro-r-02-001", "Next from challenge must advance to M02-E01")
        self.assertFalse(data["prevDisabled"], "Previous button on M02-E01 must be enabled for admin")
        self.assertEqual(data["curExAfterPrev"], "intro-r-01-008", "Previous must navigate back to M01-E08")


    # --------------------------------------------------------------------------
    # K. Landing Catalog: All 89 exercises and 13 challenges accessible
    # --------------------------------------------------------------------------
    def test_case_k_landing_catalog_all_89_exercises_and_13_challenges_accessible(self):
        """Case K: On index.html, admin sees all 89 exercises and 13 challenges as available and clickable."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                await ctx.route("**/functions/v1/**", lambda r: r.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"ok": True, "student": {"role": "admin", "isAdmin": True}})
                ))
                await ctx.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'test-admin-token-k',
                        expiresAt: new Date(Date.now() + 86400000).toISOString(),
                        student: {
                            id: '00000000-0000-4000-8000-000000000001',
                            displayName: 'Admin Katherine',
                            role: 'admin',
                            isAdmin: true,
                            section: 'TEST-ADMIN'
                        }
                    }));
                """)
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/index.html", wait_until="domcontentloaded")
                await page.wait_for_selector("#sr-course-accordion")

                res = await page.evaluate("""() => {
                    const accordion = document.getElementById('sr-course-accordion');
                    const modItems = Array.from(accordion.querySelectorAll('.sr-accordion-item'));
                    const allExItems = Array.from(accordion.querySelectorAll('.sr-exercise-item'));
                    const allChallenges = Array.from(accordion.querySelectorAll('.sr-challenge-card'));

                    let lockedExercises = 0;
                    let availableExercises = 0;
                    allExItems.forEach(el => {
                        const link = el.querySelector('a');
                        const linkStyle = link ? window.getComputedStyle(link) : null;
                        if (el.classList.contains('is-locked') || (linkStyle && linkStyle.pointerEvents === 'none')) {
                            lockedExercises++;
                        } else {
                            availableExercises++;
                        }
                    });

                    let lockedChallenges = 0;
                    let availableChallenges = 0;
                    allChallenges.forEach(el => {
                        if (el.classList.contains('is-module-locked') || el.classList.contains('is-standby')) {
                            lockedChallenges++;
                        } else {
                            availableChallenges++;
                        }
                    });

                    return {
                        ok: true,
                        totalModules: modItems.length,
                        totalExercises: allExItems.length,
                        availableExercises,
                        lockedExercises,
                        totalChallenges: allChallenges.length,
                        availableChallenges,
                        lockedChallenges
                    };
                }""")
                await browser.close()
                return res

        data = self.run_async(_test())
        self.assertTrue(data.get("ok"))
        self.assertEqual(data["totalModules"], 13, "Landing accordion must render 13 modules")
        self.assertEqual(data["totalExercises"], 89, "Landing accordion must contain exactly 89 exercises")
        self.assertEqual(data["availableExercises"], 89, "All 89 exercises must be available and clickable for admin")
        self.assertEqual(data["lockedExercises"], 0, "Zero exercises may be locked for admin")
        self.assertEqual(data["totalChallenges"], 13, "Landing accordion must contain 13 final challenges")
        self.assertEqual(data["availableChallenges"], 13, "All 13 challenges must be available for admin")
        self.assertEqual(data["lockedChallenges"], 0, "Zero challenges may be locked for admin")

    # --------------------------------------------------------------------------
    # L. Specific Screenshot Case: M05 in Landing Catalog
    # --------------------------------------------------------------------------
    def test_case_l_landing_m05_exact_capture_verification(self):
        """Case L: Module 5 on index.html shows all 8 exercises available + challenge available, no empty space."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                await ctx.route("**/functions/v1/**", lambda r: r.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"ok": True, "student": {"role": "admin", "isAdmin": True}})
                ))
                await ctx.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'test-admin-token-l',
                        expiresAt: new Date(Date.now() + 86400000).toISOString(),
                        student: {
                            id: '00000000-0000-4000-8000-000000000003',
                            displayName: 'Tomás Urzúa',
                            role: 'admin',
                            isAdmin: true,
                            section: 'TEST-ADMIN'
                        }
                    }));
                """)
                page = await ctx.new_page()
                await page.goto(f"{self.base_url}/index.html", wait_until="domcontentloaded")
                await page.wait_for_selector("#sr-header-05")

                # Expand M05
                await page.click("#sr-header-05")
                await page.wait_for_timeout(200)

                m5_data = await page.evaluate("""() => {
                    const header = document.getElementById('sr-header-05');
                    const badge = header.querySelector('.sr-module-badge');
                    const panel = document.getElementById('sr-panel-05');
                    const items = Array.from(panel.querySelectorAll('.sr-exercise-item'));
                    const chCard = panel.querySelector('.sr-challenge-card');
                    const chBtn = chCard ? chCard.querySelector('.sr-challenge-btn') : null;

                    return {
                        badgeText: badge ? badge.textContent.trim() : null,
                        badgeClass: badge ? badge.className : null,
                        challengeClass: chCard ? chCard.className : null,
                        challengeBtnText: chBtn ? chBtn.textContent.trim() : null,
                        itemsCount: items.length,
                        items: items.map(el => {
                            const link = el.querySelector('a');
                            const style = window.getComputedStyle(el);
                            const linkStyle = link ? window.getComputedStyle(link) : null;
                            const icon = el.querySelector('.sr-ex-status-icon');
                            return {
                                id: el.getAttribute('data-ex-id'),
                                className: el.className,
                                iconText: icon ? icon.textContent.trim() : null,
                                linkPointerEvents: linkStyle ? linkStyle.pointerEvents : null,
                                display: style.display,
                                opacity: style.opacity
                            };
                        })
                    };
                }""")

                # Also test direct navigation to m05 targets
                direct_tests = {}
                for target_hash in ["intro-r-05-001", "intro-r-05-004", "intro-r-05-008", "intro-r-05-challenge"]:
                    p_direct = await ctx.new_page()
                    await p_direct.goto(f"{self.base_url}/curso.html#{target_hash}")
                    await p_direct.wait_for_function(f"""() => {{
                        const el = document.querySelector('.social-r-exercise.is-active-exercise');
                        return el && el.getAttribute('data-exercise-id') === '{target_hash}';
                    }}""", timeout=10000)
                    active_info = await p_direct.evaluate("""() => {
                        const active = document.querySelector('.social-r-exercise.is-active-exercise');
                        return {
                            activeId: active ? active.getAttribute('data-exercise-id') : null,
                            isChallenge: active ? active.classList.contains('social-r-challenge') : false
                        };
                    }""")
                    direct_tests[target_hash] = active_info
                    await p_direct.close()

                await browser.close()
                return {"m5_data": m5_data, "direct_tests": direct_tests}

        res = self.run_async(_test())
        m5 = res["m5_data"]
        self.assertEqual(m5["badgeText"], "Disponible")
        self.assertEqual(m5["itemsCount"], 8, "Module 5 must contain exactly 8 exercises")
        for item in m5["items"]:
            self.assertIn("is-available", item["className"], f"{item['id']} must be available")
            self.assertEqual(item["linkPointerEvents"], "auto", f"{item['id']} must allow pointer events")
            self.assertEqual(item["iconText"], "○", f"{item['id']} must display available icon")
            self.assertEqual(item["display"], "flex", f"{item['id']} must be visible")
            self.assertEqual(item["opacity"], "1", f"{item['id']} must be full opacity")
        self.assertIn("is-available", m5["challengeClass"], "Module 5 challenge must be available")
        self.assertIn("Comenzar desafío", m5["challengeBtnText"])

        # Check direct links
        for ex_id, d_res in res["direct_tests"].items():
            self.assertEqual(d_res["activeId"], ex_id, f"Direct link to {ex_id} must open that exact activity")

    # --------------------------------------------------------------------------
    # M. Multi-Module Jumping Sequence
    # --------------------------------------------------------------------------
    def test_case_m_multi_module_jumping_sequence(self):
        """Case M: Sequence M01-E01 -> M05-E08 -> M09-Challenge -> M13-E05 -> M13-Challenge -> M03-E02."""
        sequence = [
            ("intro-r-01-001", False),
            ("intro-r-05-008", False),
            ("intro-r-09-challenge", True),
            ("intro-r-13-005", False),
            ("intro-r-13-challenge", True),
            ("intro-r-03-002", False),
        ]

        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                await ctx.route("**/functions/v1/**", lambda r: r.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"ok": True, "student": {"role": "admin", "isAdmin": True}})
                ))
                page = await ctx.new_page()

                await page.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'test-admin-token-m',
                        expiresAt: new Date(Date.now() + 86400000).toISOString(),
                        student: {
                            id: '00000000-0000-4000-8000-000000000004',
                            displayName: 'Gabriel Cortés',
                            role: 'admin',
                            isAdmin: true,
                            section: 'TEST-ADMIN'
                        }
                    }));
                """)

                results = []
                for act_id, is_ch in sequence:
                    await page.goto(f"{self.base_url}/curso.html#{act_id}")
                    await page.wait_for_function(f"""() => {{
                        const el = document.querySelector('.social-r-exercise.is-active-exercise');
                        return el && el.getAttribute('data-exercise-id') === '{act_id}';
                    }}""", timeout=10000)
                    state = await page.evaluate("""() => {
                        const active = document.querySelector('.social-r-exercise.is-active-exercise');
                        const nav = window.SocialR && window.SocialR.navigation;
                        const store = window.SocialR && window.SocialR.progress;
                        return {
                            activeDomId: active ? active.getAttribute('data-exercise-id') : null,
                            isChallenge: active ? active.classList.contains('social-r-challenge') : false,
                            navCurrentId: nav && nav.getCurrentExercise() ? nav.getCurrentExercise().id : null,
                            navActiveChId: nav && nav.activeChallenge ? nav.activeChallenge.id : null,
                            completedCount: store && store.state && store.state.modules
                                ? Object.values(store.state.modules).reduce((acc, m) => acc + (m.completedExercises ? m.completedExercises.length : 0), 0)
                                : 0
                        };
                    }""")
                    results.append(state)

                await browser.close()
                return results

        results = self.run_async(_test())
        for idx, (expected_id, is_challenge) in enumerate(sequence):
            res = results[idx]
            self.assertEqual(res["activeDomId"], expected_id, f"Step {idx}: DOM active exercise must be {expected_id}")
            self.assertEqual(res["isChallenge"], is_challenge, f"Step {idx}: Challenge status mismatch")
            # CRITICAL: Navigating between activities must NEVER auto-complete exercises!
            self.assertEqual(res["completedCount"], 0, "Admin navigation must NOT auto-complete exercises")

    # --------------------------------------------------------------------------
    # N. Regular Student & Guest Gating Preserved on Landing Catalog
    # --------------------------------------------------------------------------
    def test_case_n_regular_student_and_guest_m05_gating_preserved(self):
        """Case N: Regular student and guest have Module 5 and subsequent modules locked."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                # 1. Regular Student
                ctx_student = await browser.new_context()
                await ctx_student.route("**/functions/v1/**", lambda r: r.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"ok": True, "student": {"role": "student", "isAdmin": False}})
                ))
                p_student = await ctx_student.new_page()
                await p_student.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'test-student-token-n',
                        expiresAt: new Date(Date.now() + 86400000).toISOString(),
                        student: {
                            id: '00000000-0000-4000-8000-000000000099',
                            displayName: 'Estudiante Regular',
                            role: 'student',
                            isAdmin: false,
                            section: '1'
                        }
                    }));
                """)
                await p_student.goto(f"{self.base_url}/index.html", wait_until="domcontentloaded")
                await p_student.wait_for_selector("#sr-header-05")
                student_res = await p_student.evaluate("""() => {
                    const badge = document.querySelector('#sr-header-05 .sr-module-badge');
                    const panel = document.getElementById('sr-panel-05');
                    const items = Array.from(panel.querySelectorAll('.sr-exercise-item'));
                    const ch = panel.querySelector('.sr-challenge-card');
                    return {
                        badgeText: badge ? badge.textContent.trim() : null,
                        badgeClass: badge ? badge.className : null,
                        chClass: ch ? ch.className : null,
                        lockedCount: items.filter(el => el.classList.contains('is-locked')).length
                    };
                }""")
                await ctx_student.close()

                # 2. Guest Mode
                ctx_guest = await browser.new_context()
                await ctx_guest.route("**/functions/v1/**", lambda r: r.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"ok": False})
                ))
                p_guest = await ctx_guest.new_page()
                await p_guest.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:guest-mode', 'true');
                """)
                await p_guest.goto(f"{self.base_url}/index.html", wait_until="domcontentloaded")
                await p_guest.wait_for_selector("#sr-header-05")
                guest_res = await p_guest.evaluate("""() => {
                    const badge = document.querySelector('#sr-header-05 .sr-module-badge');
                    const panel = document.getElementById('sr-panel-05');
                    const items = Array.from(panel.querySelectorAll('.sr-exercise-item'));
                    const ch = panel.querySelector('.sr-challenge-card');
                    return {
                        badgeText: badge ? badge.textContent.trim() : null,
                        badgeClass: badge ? badge.className : null,
                        chClass: ch ? ch.className : null,
                        lockedCount: items.filter(el => el.classList.contains('is-locked')).length
                    };
                }""")
                await ctx_guest.close()

                await browser.close()
                return {"student": student_res, "guest": guest_res}

        data = self.run_async(_test())
        # Student
        self.assertEqual(data["student"]["badgeText"], "Bloqueado")
        self.assertIn("is-locked", data["student"]["badgeClass"])
        self.assertIn("is-module-locked", data["student"]["chClass"])
        self.assertEqual(data["student"]["lockedCount"], 8, "Regular student must have all 8 M05 exercises locked")

        # Guest
        self.assertEqual(data["guest"]["badgeText"], "Bloqueado")
        self.assertIn("is-locked", data["guest"]["badgeClass"])
        self.assertIn("is-module-locked", data["guest"]["chClass"])
        self.assertEqual(data["guest"]["lockedCount"], 8, "Guest must have all 8 M05 exercises locked")

    # --------------------------------------------------------------------------
    # O. Admin Logout -> Regular Student Login: No Privilege Leakage
    # --------------------------------------------------------------------------
    def test_case_o_logout_restores_strict_gating(self):
        """Case O: Admin logout -> regular student login completely revokes admin privileges."""
        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context()
                page = await ctx.new_page()

                # Step 1: Admin session
                await page.add_init_script("""
                    localStorage.setItem('social-r:tour-completed', 'true');
                    localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'test-admin-token-o',
                        expiresAt: new Date(Date.now() + 86400000).toISOString(),
                        student: {
                            id: '00000000-0000-4000-8000-000000000002',
                            displayName: 'Juan Carlos',
                            role: 'admin',
                            isAdmin: true,
                            section: 'TEST-ADMIN'
                        }
                    }));
                """)
                await page.goto(f"{self.base_url}/curso.html", wait_until="domcontentloaded")
                await page.wait_for_selector(".social-r-exercise.is-active-exercise")

                admin_status = await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    return {
                        cloudIsAdmin: cloud && cloud.isAdmin(),
                        m13Unlocked: config && config.isModuleUnlocked('13-de-la-pregunta-al-analisis')
                    };
                }""")

                # Step 2: Logout and clear session
                await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    if (cloud) cloud.clearSession();
                }""")

                # Step 3: Regular student login
                await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    if (cloud) {
                        cloud.setSession({
                            sessionToken: 'test-student-token-o2',
                            expiresAt: new Date(Date.now() + 86400000).toISOString(),
                            student: {
                                id: '00000000-0000-4000-8000-000000000088',
                                displayName: 'Estudiante Nuevo',
                                role: 'student',
                                isAdmin: false,
                                section: '2'
                            }
                        });
                    }
                }""")

                student_status = await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    const config = window.SocialR && window.SocialR.courseConfig;
                    return {
                        cloudIsAdmin: cloud && cloud.isAdmin(),
                        m13Unlocked: config && config.isModuleUnlocked('13-de-la-pregunta-al-analisis')
                    };
                }""")

                await browser.close()
                return {"admin": admin_status, "student": student_status}

        data = self.run_async(_test())
        self.assertTrue(data["admin"]["cloudIsAdmin"])
        self.assertTrue(data["admin"]["m13Unlocked"])
        self.assertFalse(data["student"]["cloudIsAdmin"], "Regular student must not have admin privilege")
        self.assertFalse(data["student"]["m13Unlocked"], "Module 13 must be locked for new regular student")


if __name__ == "__main__":
    unittest.main()

