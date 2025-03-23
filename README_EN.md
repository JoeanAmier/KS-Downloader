<div align="center">
<img src="docs/KS-Downloader.png" alt="TikTokDownloader" height="256" width="256"><br>
<h1>KS-Downloader</h1>
<p>English | <a href="README.md">简体中文</a></p>
<img alt="GitHub" src="https://img.shields.io/github/license/JoeanAmier/KS-Downloader?style=for-the-badge&color=ff7a45">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/JoeanAmier/KS-Downloader?style=for-the-badge&color=fa8c16">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/JoeanAmier/KS-Downloader?style=for-the-badge&color=ffee6f">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/JoeanAmier/KS-Downloader?style=for-the-badge&color=13c2c2">
<br>
<img alt="Static Badge" src="https://img.shields.io/badge/Python-3.12-3498db?style=for-the-badge&logo=python&labelColor=fffa65">
<img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/JoeanAmier/KS-Downloader?style=for-the-badge&color=f759ab">
<img src="https://img.shields.io/badge/Sourcery-enabled-884898?style=for-the-badge&color=1890ff" alt="">
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/JoeanAmier/KS-Downloader/total?style=for-the-badge&color=52c41a">
<br>
<p>🔥 <b>KuaiShou Works Download Tool: </b>Completely free and open-source, based on HTTPX module, for downloading KuaiShou watermark-free video and image files!</p>
<p>⭐ This project is completely free and open-source with no paid features. Beware of scams!</p>
<p>⭐ Due to the author's limited energy, I was unable to update the English document in a timely manner, and the content may have become outdated, partial translation is machine translation, the translation result may be incorrect, Suggest referring to Chinese documentation. If you want to contribute to translation, we warmly welcome you.</p>
</div>
<hr>
<h1>📑 Project Features</h1>
<ul>
<li>✅ Download watermark-free KuaiShou works</li>
<li>☑️ Download works cover images</li>
<li>☑️ Download works music files</li>
<li>✅ Auto-skip downloaded files</li>
<li>✅ File integrity verification</li>
<li>✅ Persistent works metadata storage</li>
<li>✅ Track downloaded works IDs</li>
<li>✅ Resumable downloads</li>
<li>✅ Dedicated storage folders</li>
<li>✅ Custom filename formats</li>
<li>✅ Browser cookie extraction</li>
<li>✅ Author alias configuration</li>
<li>✅ Archive works by author</li>
<li>✅ Automatic author nickname updates</li>
<li>☑️ Background clipboard monitoring</li>
<li>☑️ CLI support</li>
<li>☑️ API integration</li>
</ul>
<p>⭐ Check KS-Downloader development plans and progress at <a href="https://github.com/users/JoeanAmier/projects/6">Projects</a></p>
<h1>📸 Screenshots</h1>
<p><b>🎥 Click images to watch demo video</b></p>
<a href="https://www.bilibili.com/video/BV19YC4Y7E8E/"><img src="docs/项目运行截图1.png" alt=""></a>
<hr>
<a href="https://www.bilibili.com/video/BV19YC4Y7E8E/"><img src="docs/项目运行截图2.png" alt=""></a>
<h1>🥣 Usage Guide</h1>
<h2>🖱 Application Execution</h2>
<p>⭐ Mac OS/Windows 10+ users: Download pre-built packages from <a href="https://github.com/JoeanAmier/KS-Downloader/releases/latest">Releases</a> or <a href="https://github.com/JoeanAmier/KS-Downloader/actions">Actions</a>. Extract and double-click <code>main</code> to run!</p>
<p>⭐ This project includes GitHub Actions for automatic builds - users can compile latest source code into executables anytime!</p>
<p><strong>Note: Mac OS executable <code>main</code> may require terminal execution. Limited by testing devices, Mac version hasn't been fully validated.</strong></p>
<p>Default download path: <code>.\_internal\Download</code><br>Configuration file: <code>.\_internal\config.yaml</code></p>
<h3>Update Methods</h3>
<p> <strong>Method 1:</strong> Download and extract the new version, copy previous version's <code>KS-Downloader.db</code> and <code>config.yaml</code> to <code>_internal</code> folder.</p>
<p> <strong>Method 2:</strong> Download new version (don't execute), overwrite all old files directly by copying entire contents.</p>
<h2>⌨️ Source Code Execution</h2>
<ol>
<li>Install Python interpreter version <code>3.12</code></li>
<li>Download latest source code from repository or <a href="https://github.com/JoeanAmier/KS-Downloader/releases/latest">Releases</a></li>
<li>Open terminal and navigate to project root directory</li>
<li>Install dependencies: <code>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt</code></li>
<li>Execute <code>main.py</code> to start</li>
</ol>
<h2>⌨️ Docker Execution</h2>
<ol>
<li>Obtain image:
<ul>
<li>Method 1: Build using <code>Dockerfile</code></li>
<li>Method 2: Pull image via <code>docker pull joeanamier/ks-downloader</code></li>
</ul>
</li>
<li>Create container: <code>docker run --name [container_name(optional)] -it joeanamier/ks-downloader</code></li>
<li>Container operations:
<ul>
<li>Start: <code>docker start -i [container_name/ID]</code></li>
<li>Restart: <code>docker restart -i [container_name/ID]</code></li>
</ul>
</li>
</ol>
<p><b>Note:</b> Docker version doesn't support <b>browser cookie reading</b> and <b>clipboard monitoring</b>. Other features remain functional. Please report any anomalies.</p>
<h1>🔗 Supported Links</h1>
<ul>
<li><code>https://www.kuaishou.com/f/share-code</code></li>
<li><code>https://v.kuaishou.com/share-code</code></li>
<li><code>https://www.kuaishou.com/short-video/worksID</code></li>
<li><code>https://kuaishou.cn/short-video/worksID</code></li>
<li><code>https://live.kuaishou.com/u/author-id/worksID</code></li>
<br/>
<p><b>Recommend using share links; Multiple URLs supported (space separated).</b></p>
</ul>

<h1>🪟 Terminal Recommendation</h1>
<p>⭐ Use <a href="https://learn.microsoft.com/zh-cn/windows/terminal/install">Windows Terminal</a> (default on Windows 11) for optimal display!</p>

<h1>📜 Additional Notes</h1>
<ul>
<li>Windows requires admin privileges to read Chromium/Chrome/Edge cookies</li>
<li>Work data stored in <code>./Data/DetailData.db</code> when enabled</li>
<li>Settings and download records in <code>./KS-Downloader.db</code></li>
</ul>

<h1>⚙️ Configuration File</h1>
<p><code>config.yaml</code> (auto-generated) allows custom settings:</p>
<p><strong>If features malfunction, configure cookies first!</strong></p>
<table>
<thead>
<tr>
<th align="center">Parameter</th>
<th align="center">Type</th>
<th align="center">Description</th>
<th align="center">Default</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">work_path</td>
<td align="center">str</td>
<td align="center">Root path for work data/file storage</td>
<td align="center">Project root directory</td>
</tr>
<tr>
<td align="center">folder_name</td>
<td align="center">str</td>
<td align="center">Storage folder name for works files</td>
<td align="center">Download</td>
</tr>
<tr>
<td align="center">name_format</td>
<td align="center">str</td>
<td align="center"><sup><a href="#fields">#</a></sup>Filename format using space-separated fields. Supported fields: <code>作品类型</code>、<code>作者昵称</code>、<code>作者ID</code>、<code>作品描述</code>、<code>作品ID</code>、<code>发布日期</code></td>
<td align="center"><code>发布日期 作者昵称 作品描述</code></td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">str</td>
<td align="center">KuaiShou web interface Cookie <b>(no login required)</b></td>
<td align="center">Dynamically fetched</td>
</tr>
<tr>
<td align="center">proxy</td>
<td align="center">str</td>
<td align="center">Set program proxy</td>
<td align="center">null</td>
</tr>
<tr>
<td align="center">data_record</td>
<td align="center">bool</td>
<td align="center">Save works data to file (SQLite format)</td>
<td align="center">false</td>
</tr>
<tr>
<tr>
<td align="center">max_workers</td>
<td align="center">int</td>
<td align="center">Maximum concurrent download tasks</td>
<td align="center">4</td>
</tr>
<tr>
<td align="center"><del>cover</del></td>
<td align="center">str</td>
<td align="center">Cover download format (JPEG/WEBP), empty string disables</td>
<td align="center">Empty string</td>
</tr>
<tr>
<td align="center"><del>music</del></td>
<td align="center">bool</td>
<td align="center">Download works music track</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">max_retry</td>
<td align="center">int</td>
<td align="center">Max retry attempts on failure (seconds)</td>
<td align="center">5</td>
</tr>
<tr>
<td align="center">timeout</td>
<td align="center">int</td>
<td align="center">Request timeout limit (seconds)</td>
<td align="center">10</td>
</tr>
<tr>
<td align="center">chunk</td>
<td align="center">int</td>
<td align="center">Download chunk size in bytes</td>
<td align="center">2097152 (2 MB)</td>
</tr>
<tr>
<td align="center">folder_mode</td>
<td align="center">bool</td>
<td align="center">Store files in individual folders (folder matches filename)</td>
<td align="center">false</td>
</tr>
</tbody>
</table>
<div id="fields">
<p>name_format instructions (Currently only supports Chinese values) :</p>
<ul>
<li><code>作品ID</code>: Works ID</li>
<li><code>作品描述</code>: Works Description</li>
<li><code>作品类型</code>: Works Type</li>
<li><code>发布时间</code>: Publish Time</li>
<li><code>作者昵称</code>: Author Nickname</li>
<li><code>作者ID</code>: Author ID</li>
</ul>
</div>

# 📦 Build of Executable File Guide

This guide will walk you through forking this repository and executing GitHub Actions to automatically build and package
the program based on the latest source code!

---

## Steps to Use

### 1. Fork the Repository

1. Click the **Fork** button at the top right of the project repository to fork it to your personal GitHub account
2. Your forked repository address will look like this: `https://github.com/your-username/this-repo`

---

### 2. Enable GitHub Actions

1. Go to the page of your forked repository
2. Click the **Settings** tab at the top
3. Click the **Actions** tab on the right
4. Click the **General** option
5. Under **Actions permissions**, select **Allow all actions and reusable workflows** and click the **Save** button

---

### 3. Manually Trigger the Build Process

1. In your forked repository, click the **Actions** tab at the top
2. Find the workflow named **构建可执行文件**
3. Click the **Run workflow** button on the right:
    - Select the **master** or **develop** branch
    - Click **Run workflow**

---

### 4. Check the Build Progress

1. On the **Actions** page, you can see the execution records of the triggered workflow
2. Click on the run record to view detailed logs to check the build progress and status

---

### 5. Download the Build Result

1. Once the build is complete, go to the corresponding run record page
2. In the **Artifacts** section at the bottom of the page, you will see the built result file
3. Click to download and save it to your local machine to get the built program

---

## Notes

1. **Resource Usage**:
    - GitHub provides free build environments for Actions, with a monthly usage limit (2000 minutes) for free-tier
      users

2. **Code Modifications**:
    - You are free to modify the code in your forked repository to customize the build process
    - After making changes, you can trigger the build process again to get your customized version

3. **Stay in Sync with the Main Repository**:
    - If the main repository is updated with new code or workflows, it is recommended that you periodically sync your
      forked repository to get the latest features and fixes

---

## Frequently Asked Questions

### Q1: Why can't I trigger the workflow?

A: Please ensure that you have followed the steps to **Enable Actions**. Otherwise, GitHub will prevent the workflow
from running

### Q2: What should I do if the build process fails?

A:

- Check the run logs to understand the cause of the failure
- Ensure there are no syntax errors or dependency issues in the code
- If the problem persists, please open an issue on
  the [Issues page](https://github.com/JoeanAmier/KS-Downloader/issues)

### Q3: Can I directly use the Actions from the main repository?

A: Due to permission restrictions, you cannot directly trigger Actions from the main repository. Please use the forked
repository to execute the build process

<h1>⚠️ Disclaimer</h1>
<ul>
<li>Users decide on their own how to use this project and bear the risks themselves. The author is not responsible for any losses, liabilities, or risks incurred by users in the use of this project</li>
<li>The code and functionalities provided by the author of this project are developed based on existing knowledge and technology. The author strives to ensure the correctness and security of the code but does not guarantee that the code is completely error-free or defect-free.</li>
<li>Users must strictly adhere to the provisions in <a href="https://github.com/JoeanAmier/KS-Downloader/blob/master/LICENSE">GNU
    General Public License v3.0</a> , and appropriately mention the use of code adhering <a
        href="https://github.com/JoeanAmier/KS-Downloader/blob/master/LICENSE">GNU General Public License
    v3.0</a>.
</li>
<li>Under no circumstances shall users associate the author of this project, contributors, or other related parties with the user's usage behavior, or demand that they be held responsible for any losses or damages incurred by the user's use of this project.</li>
<li>Users must independently study relevant laws and regulations when using the code and functionalities of this project and ensure that their usage is legal and compliant. Users are solely responsible for any legal liability and risks resulting from violations of laws and regulations.</li>
<li>The author of this project will not provide a paid version of the KS-Downloader project, nor will they offer any commercial services related to the KS-Downloader project.</li>
<li>Any secondary development, modification, or compilation of the program based on this project is unrelated to the original author. The original author is not responsible for any consequences related to secondary development or its results. Users should take full responsibility for any situations that may arise from secondary development on their own.</li>
</ul>
<b>Before using the code and functionalities of this project, please carefully consider and accept the above disclaimer. If you have any questions or disagree with the statement, please do not use the code and functionalities of this project. If you use the code and functionalities of this project, it is considered that you fully understand and accept the above disclaimer, and willingly assume all risks and consequences associated with the use of this project.</b>

<h1>✉️ Contact the Author</h1>
<ul>
<li>Author's Email：yonglelolu@foxmail.com</li>
<li>Author's WeChat: Downloader_Tools</li>
<li><b>Discord Community</b>: <a href="https://discord.com/invite/ZYtmgKud9Y">Click to Join the Community</a></li>
</ul>
<p>✨ <b>Other Open Source Projects by the Author:</b></p>
<ul>
<li><b>TikTokDownloader（抖音、TikTok）</b>：<a href="https://github.com/JoeanAmier/TikTokDownloader">https://github.com/JoeanAmier/TikTokDownloader</a></li>
<li><b>XHS-Downloader（小红书、XiaoHongShu、RedNote）</b>：<a href="https://github.com/JoeanAmier/XHS-Downloader">https://github.com/JoeanAmier/XHS-Downloader</a></li>
</ul>

<h1>♥️ Support the Project</h1>
<p>If <b>KS-Downloader</b> has been helpful to you, please consider giving it a <b>Star</b> ⭐. Thank you for your support!</p>
<table>
<thead>
<tr>
<th align="center">微信(WeChat)</th>
<th align="center">支付宝(Alipay)</th>
</tr>
</thead>
<tbody><tr>
<td align="center"><img src="./docs/微信赞助二维码.png" alt="微信赞助二维码" height="200" width="200"></td>
<td align="center"><img src="./docs/支付宝赞助二维码.png" alt="支付宝赞助二维码" height="200" width="200"></td>
</tr>
</tbody>
</table>
<p>If you are willing, you may consider making a donation to provide additional support for <b>KS-Downloader</b>!</p>
<h1>🌟 Contribution Guidelines</h1>
<p><strong>Welcome to contributing to this project! To keep the codebase clean, efficient, and easy to maintain, please read the following guidelines carefully to ensure that your contributions can be accepted and integrated smoothly.</strong></p>
<ul>
<li>Before starting development, please pull the latest code from the <code>develop</code> branch as the basis for your modifications; this helps avoid merge conflicts and ensures your changes are based on the latest state of the project.</li>
<li>If your changes involve multiple unrelated features or issues, please split them into several independent commits or pull requests.</li>
<li>Each pull request should focus on a single feature or fix as much as possible, to facilitate code review and testing.</li>
<li>Follow the existing coding style; make sure your code is consistent with the style already present in the project.</li>
<li>Write code that is easy to read; add appropriate annotation to help others understand your intentions.</li>
<li>Each commit should include a clear and concise commit message describing the changes made. The commit message should follow this format: <code>&lt;type&gt;: &lt;short description&gt;</code></li>
<li>When you are ready to submit a pull request, please prioritize submitting them to the <code>develop</code> branch; this provides maintainers with a buffer zone for additional testing and review before final merging into the <code>master</code> branch.</li>
</ul>
<p><strong>Reference materials:</strong></p>
<ul>
<li><a href="https://www.contributor-covenant.org/version/2/1/code_of_conduct/">Contributor Covenant</a></li>
<li><a href="https://opensource.guide/how-to-contribute/">How to Contribute to Open Source</a></li>
</ul>
<h1>💰 Sponsor</h1>
<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm.svg" alt="PyCharm logo">
<p><b>JetBrains</b> support active projects recognized within the global open-source community with complimentary licenses for non-commercial development.</p>

# 💡 Project References

* https://github.com/moyada/stealer
* https://github.com/encode/httpx/
* https://github.com/Textualize/rich
* https://github.com/Tinche/aiofiles
* https://github.com/omnilib/aiosqlite
* https://github.com/pyinstaller/pyinstaller
* https://github.com/thewh1teagle/rookie
* https://github.com/lxml/lxml
* https://github.com/yaml/pyyaml
* https://github.com/carpedm20/emoji/
