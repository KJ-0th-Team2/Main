/**
 * <jungle-nav> — Shadow DOM 없는 버전 (Light DOM)
 * Tailwind CDN과 완벽 호환
 *
 * 사용법:
 *   <script src="jungle-nav.js"></script>
 *   <jungle-nav logo-text="정글 위키" logo-href="/"></jungle-nav>
 */
class JungleNav extends HTMLElement {
  static get observedAttributes() {
    return ["logo-text", "logo-href", "active-page"];
  }
  constructor() {
    super();
    this._escBound = false;
    this._notifications = [];
  }

  connectedCallback() {
    this._render();
  }

  attributeChangedCallback() {
    this._render();
  }
  _unreadCount() {
    return this._notifications.filter(n => !n.read).length;
  }
  _render() {
    const logoText = this.getAttribute("logo-text") || "정글 위키";
    const logoHref = this.getAttribute("logo-href") || "/";
    const unread   = this._unreadCount();
    this.innerHTML = `
      <!-- ── 모달 오버레이 ── -->
      <div id="jn-modal-overlay"
        class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
        <div id="jn-modal-card"
          class="relative w-full max-w-sm mx-4 bg-white rounded-2xl shadow-2xl px-10 py-12">
        </div>
      </div>

      <!-- ── 네비게이션 바 ── -->
      <nav class="flex justify-between items-center p-6 bg-white shadow">
        <a href="${logoHref}" class="font-bold text-xl text-gray-900 no-underline">${logoText}</a>
        <div class="flex items-center gap-x-8">
          <!-- 알림 -->
                      <div class="relative" id="jn-noti-wrapper">
            <button id="jn-noti-btn"
              class="relative text-gray-500 hover:text-blue-600 bg-transparent border-none cursor-pointer flex items-center"
              aria-label="알림">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
              </svg>
              ${unread > 0 ? `
              <span id="jn-noti-badge"
                class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                ${unread > 9 ? '9+' : unread}
              </span>` : ''}
            </button>

            <!-- 알림 팝업 -->
            <div id="jn-noti-popup"
              class="hidden absolute right-0 top-full mt-2 w-80 bg-white rounded-xl shadow-xl border border-gray-100 z-50 overflow-hidden">
              <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
                <span class="text-sm font-semibold text-gray-800">알림</span>
                ${unread > 0 ? `
                <button id="jn-noti-read-all"
                  class="text-xs text-blue-500 hover:text-blue-700 bg-transparent border-none cursor-pointer">
                  모두 읽음
                </button>` : ''}
              </div>
              <ul id="jn-noti-list" class="max-h-72 overflow-y-auto divide-y divide-gray-50">
                ${this._renderNotificationItems()}
              </ul>
            </div>
          </div>
          <!-- 검색 -->
          <a href="#" id="jn-search-trigger" class="text-gray-500 hover:text-blue-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
              stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </a>
                    <input type="text" id="jn-search-input"
                class="hidden border border-gray-300 rounded px-2 py-1 ml-2"
                placeholder="검색어를 입력하세요" />
          <!-- 로그인 -->
          <button id="jn-login-trigger"
            class="text-gray-500 hover:text-blue-600 bg-transparent border-none cursor-pointer text-base">
            로그인
          </button>
        </div>
      </nav>
    `;

    // 이벤트 바인딩
    this.querySelector("#jn-login-trigger").addEventListener("click", () =>
      this._openModal("login"),
    );
    const searchTrigger = this.querySelector('#jn-search-trigger');
    const searchInput = this.querySelector('#jn-search-input');
    // 검색 input 토글
    searchTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      searchInput.classList.toggle('hidden');
      if(!searchInput.classList.contains('hidden')) searchInput.focus();
    });
    // 검색 Enter 이벤트
    searchInput.addEventListener('keydown', async (e) => {
      if(e.key === 'Enter'){
        const keyword = searchInput.value.trim();
        if(keyword){
          console.log('검색어:',keyword);
          // 여기에 AJAX 호출 넣으면 서버 검색 가능
          // 예시: await fetch(`/search?keyword=${keyword}`)
        }
        searchInput.value='';
        searchInput.classList.add('hidden');
      }
    });

    document.addEventListener('click', (e) =>{
      const isClickInside = this.contains(e.target);
      if(!isClickInside){
        searchInput.classList.add('hidden');
      }
    });
    const overlay = this.querySelector("#jn-modal-overlay");
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) this._closeModal();
    });

    // 알림 버튼 토글
    this.querySelector('#jn-noti-btn')
      .addEventListener('click', (e) => {
        e.stopPropagation();
        this._toggleNotiPopup();
      });

    // 모두 읽음 버튼
    const readAllBtn = this.querySelector('#jn-noti-read-all');
    if (readAllBtn) {
      readAllBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this._markAllRead();
      });
    }

    // 개별 알림 클릭 → 읽음 처리
    this.querySelectorAll('.jn-noti-item').forEach(item => {
      item.addEventListener('click', () => {
        const id = Number(item.dataset.id);
        this._markRead(id);
      });
    });
    // 팝업 바깥 클릭 시 닫기
    document.addEventListener('click', (e) => {
      const wrapper = this.querySelector('#jn-noti-wrapper');
      if (wrapper && !wrapper.contains(e.target)) {
        this._closeNotiPopup();
      }
    });

    // ESC 키 (중복 등록 방지)
    if (!this._escBound) {
      this._escHandler = (e) => {
        if (e.key === "Escape") {
          this._closeModal();
          this._closeNotiPopup();
        }
      };
      document.addEventListener("keydown", this._escHandler);
      this._escBound = true;
    }
        // 쿼리셀렉터로 토큰 테스트
    this.querySelector('#token-test').addEventListener('click', async () => {
      const access_token = localStorage.getItem('access_token')

      const response = await fetch ('/auth/tokentest', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        }
      })
      console.log(response.status);

      const data = await response.json();

      if (response.ok) {
        console.log('토큰 유효', data);
      } else {
        console.log('뭔가 문제 있음');
        console.log('재발급 요청 시작');

        const refresh = await fetch ('/auth/refresh', {
          method: 'POST',
          credentials: 'include'
        })

        console.log("1차 검증");

        const refreshData = await refresh.json();

        if (refresh.status == 401) {
          alert('로그인을 해주세요.');
        } else if (refresh.status == 200) {
          alert('토큰 재발급 성공', refreshData.access_token);
          localStorage.setItem('access_token', refreshData.access_token);
        }
      }
    });
  }

  disconnectedCallback() {
    if (this._escHandler)
      document.removeEventListener("keydown", this._escHandler);
  }
  _renderNotificationItems() {
    if (this._notifications.length === 0) {
      return `<li class="px-4 py-8 text-center text-sm text-gray-400">새로운 알림이 없습니다.</li>`;
    }
    return this._notifications.map(n => `
      <li data-id="${n.id}"
        class="jn-noti-item flex items-start gap-3 px-4 py-3 cursor-pointer transition-colors
               ${n.read ? 'bg-white hover:bg-gray-50' : 'bg-blue-50 hover:bg-blue-100'}">
        <span class="mt-1.5 w-2 h-2 rounded-full flex-shrink-0 ${n.read ? 'bg-transparent' : 'bg-blue-500'}"></span>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-gray-800">
            <span class="font-semibold">${n.commenter}</span>님이
            <span class="font-semibold">'${n.postTitle}'</span>에 댓글을 남겼습니다.
          </p>
          <p class="text-xs text-gray-400 mt-0.5">${n.time}</p>
        </div>
      </li>
    `).join('');
  }
  /* ── 알림 팝업 ── */
  _toggleNotiPopup() {
    const popup = this.querySelector('#jn-noti-popup');
    popup.classList.toggle('hidden');
  }

  _closeNotiPopup() {
    const popup = this.querySelector('#jn-noti-popup');
    if (popup) popup.classList.add('hidden');
  }

  _markRead(id) {
    const noti = this._notifications.find(n => n.id === id);
    if (noti) {
      noti.read = true;
      this._render(); // 뱃지·스타일 갱신
      // 팝업 다시 열기
      const popup = this.querySelector('#jn-noti-popup');
      if (popup) popup.classList.remove('hidden');
    }
  }

  _markAllRead() {
    this._notifications.forEach(n => n.read = true);
    this._render();
    const popup = this.querySelector('#jn-noti-popup');
    if (popup) popup.classList.remove('hidden');
  }

  /**
   * 외부에서 알림을 추가할 때 호출
   * @param {{ id, postTitle, commenter, time }} noti
   */
  addNotification(noti) {
    this._notifications.unshift({ ...noti, read: false });
    this._render();
  }

  /**
   * 외부에서 알림 목록 전체를 교체할 때 호출 (API 연동용)
   * @param {Array} list
   */
  setNotifications(list) {
    this._notifications = list;
    this._render();
  }

  /* ── 모달 ── */
  _openModal(type) {
    const overlay = this.querySelector("#jn-modal-overlay");
    const card = this.querySelector("#jn-modal-card");

    card.innerHTML =
      type === "login" ? this._loginTemplate() : this._signupTemplate();
    overlay.classList.remove("hidden");
    document.body.style.overflow = "hidden";

    card
      .querySelector("#jn-close-btn")
      .addEventListener("click", () => this._closeModal());

    if (type === "login") {
      card
        .querySelector("#jn-submit-btn")
        .addEventListener("click", () => this._handleLogin());
      card
        .querySelector("#jn-switch-link")
        .addEventListener("click", () => this._openModal("signup"));
    } else {
      card
        .querySelector("#jn-submit-btn")
        .addEventListener("click", () => this._handleSignup());
      card
        .querySelector("#jn-switch-link")
        .addEventListener("click", () => this._openModal("login"));
    }
  }

  _closeModal() {
    this.querySelector("#jn-modal-overlay").classList.add("hidden");
    document.body.style.overflow = "";
  }

  /* ── 템플릿 ── */
  _loginTemplate() {
    return `
      <button id="jn-close-btn" aria-label="닫기"
        class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center
               rounded-full text-gray-400 hover:text-gray-700 hover:bg-gray-100
               active:scale-90 transition-all duration-150 bg-transparent border-none cursor-pointer">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h2 class="text-center text-3xl font-bold tracking-[0.2em] uppercase mb-10 text-gray-900">LOGIN</h2>
      <div class="flex flex-col gap-3 mb-5">
        <input id="jn-user-id" type="text" placeholder="아이디"
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800
                 placeholder-gray-400 bg-gray-50 focus:outline-none focus:border-gray-800
                 focus:ring-2 focus:ring-gray-800/10 transition-all duration-150" />
        
        <input id="jn-user-pw" type="password" placeholder="비밀번호"
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800
                 placeholder-gray-400 bg-gray-50 focus:outline-none focus:border-gray-800
                 focus:ring-2 focus:ring-gray-800/10 transition-all duration-150" />
        <p id="jn-login-error" class="hidden -mt-1 pl-1 text-xs text-red-500"></p>
      </div>
      <button id="jn-submit-btn"
        class="w-full bg-gray-900 text-white font-medium text-sm tracking-wide
               rounded-xl py-3.5 mb-4 hover:bg-gray-700 active:scale-[0.98]
               transition-all duration-150 cursor-pointer border-none">
        정글위키 로그인
      </button>
      <p id="jn-switch-link"
        class="text-right text-xs text-gray-400 hover:text-gray-700 cursor-pointer transition-colors duration-150">
        회원가입
      </p>
    `;
  }

  _signupTemplate() {
    return `
      <button id="jn-close-btn" aria-label="닫기"
        class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center
               rounded-full text-gray-400 hover:text-gray-700 hover:bg-gray-100
               active:scale-90 transition-all duration-150 bg-transparent border-none cursor-pointer">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h2 class="text-center text-3xl font-bold tracking-[0.2em] uppercase mb-10 text-gray-900">SIGN UP</h2>
      <div class="flex flex-col gap-3 mb-5">
        <input id="jn-su-id" type="text" placeholder="아이디 (4~20자 이상 소문자,숫자)"
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800
                 placeholder-gray-400 bg-gray-50 focus:outline-none focus:border-gray-800
                 focus:ring-2 focus:ring-gray-800/10 transition-all duration-150" />
        <p id="jn-su-id-error" class="hidden -mt-1 pl-1 text-xs text-red-500"></p>

        <input id="jn-su-pw" type="password" placeholder="비밀번호 (4~20자 영어,숫자,특수문자)"
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800
                 placeholder-gray-400 bg-gray-50 focus:outline-none focus:border-gray-800
                 focus:ring-2 focus:ring-gray-800/10 transition-all duration-150" />
        <p id="jn-su-pw-error" class="hidden -mt-1 pl-1 text-xs text-red-500"></p>

        <input id="jn-su-student" type="text" placeholder="학생번호"
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-800
                 placeholder-gray-400 bg-gray-50 focus:outline-none focus:border-gray-800
                 focus:ring-2 focus:ring-gray-800/10 transition-all duration-150" />
      </div>
      <button id="jn-submit-btn"
        class="w-full bg-gray-900 text-white font-medium text-sm tracking-wide
               rounded-xl py-3.5 mb-4 hover:bg-gray-700 active:scale-[0.98]
               transition-all duration-150 cursor-pointer border-none">
        회원가입
      </button>
      <p id="jn-switch-link"
        class="text-right text-xs text-gray-400 hover:text-gray-700 cursor-pointer transition-colors duration-150">
        이미 계정이 있으신가요? 로그인
      </p>
    `;
  }

  /* ── 핸들러 ── */
  async _handleLogin() {
    const id = this.querySelector("#jn-user-id").value.trim();
    const pw = this.querySelector("#jn-user-pw").value.trim();
    const errorEl = this.querySelector("#jn-login-error"); // 💡 에러 요소 참조

    // 초기화
    errorEl.classList.add("hidden");
    errorEl.textContent = "";

    if (!id || !pw) {
      errorEl.textContent = "아이디와 비밀번호를 입력해주세요.";
      errorEl.classList.remove("hidden");
      return;
    }

    try {
      const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_id: id, input_pwd: pw }),
      });
      const data = await res.json();

      if (data.result === "success") {
        this.dispatchEvent(
          new CustomEvent("jungle-login", {
            detail: { userId: id, msg: data.msg },
            bubbles: true,
          }),
        );
        alert(`${id}님, 환영합니다!`);
        localStorage.setItem("access_token", data.access_token);
        this._closeModal();
      } else {
        // 💡 alert 대신 화면에 빨간 메시지 출력
        errorEl.textContent = data.msg || "아이디 또는 비밀번호를 확인하세요.";
        errorEl.classList.remove("hidden");
      }
    } catch (err) {
      console.error(err);
      errorEl.textContent = "서버와 통신 중 오류가 발생했습니다.";
      errorEl.classList.remove("hidden");
    }
  }

  _handleSignup() {
    const id = this.querySelector("#jn-su-id").value.trim();
    const pw = this.querySelector("#jn-su-pw").value.trim();
    const student = this.querySelector("#jn-su-student").value.trim();

    // 에러 메시지 요소 가져오기 및 초기화
    const idErrorEl = this.querySelector("#jn-su-id-error");
    const pwErrorEl = this.querySelector("#jn-su-pw-error"); // 💡 추가됨

    idErrorEl.classList.add("hidden");
    idErrorEl.textContent = "";
    pwErrorEl.classList.add("hidden"); // 💡 추가됨
    pwErrorEl.textContent = ""; // 💡 추가됨

    if (!id || !pw || !student) {
      alert("모든 항목을 입력해주세요.");
      return;
    }
    // 4~20자 이상 소문자,숫자
    const idRegExp = /^[a-z0-9]{4,20}$/;
    // 4~20자 영어,숫자,특수문자
    const pwRegExp = /^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"'<>,.?/|\\~-]{4,20}$/;

    if (!idRegExp.test(id)) {
      idErrorEl.textContent =
        "아이디는 4~20자의 영문 소문자와 숫자만 사용 가능합니다.";
      idErrorEl.classList.remove("hidden");
      this.querySelector("#jn-su-id").focus();
      return;
    }

    if (!pwRegExp.test(pw)) {
      // 💡 비밀번호 에러 텍스트 출력 후 hidden 해제
      pwErrorEl.textContent = "비밀번호 형식이 올바르지 않습니다.";
      pwErrorEl.classList.remove("hidden");
      this.querySelector("#jn-su-pw").focus(); // 입력창에 다시 포커스
      return;
    }

    this.dispatchEvent(
      new CustomEvent("jungle-signup", {
        detail: { userId: id, studentId: student },
        bubbles: true,
      }),
    );

    alert(`${id}님, 회원가입 완료!`);
    this._closeModal();
  }
}

customElements.define("jungle-nav", JungleNav);
