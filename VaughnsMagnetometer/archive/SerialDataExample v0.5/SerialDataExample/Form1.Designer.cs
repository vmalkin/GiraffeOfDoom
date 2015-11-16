namespace SerialDataExample
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.ComPortDropdown = new System.Windows.Forms.ComboBox();
            this.ComConnect = new System.Windows.Forms.Button();
            this.ComDisconnect = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.configurationToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.configureHelmholtzCoilToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.helpFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutSerialCatcherToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.lblStatus = new System.Windows.Forms.Label();
            this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.configureComPortToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip1.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // ComPortDropdown
            // 
            this.ComPortDropdown.FormattingEnabled = true;
            this.ComPortDropdown.Location = new System.Drawing.Point(12, 31);
            this.ComPortDropdown.Name = "ComPortDropdown";
            this.ComPortDropdown.Size = new System.Drawing.Size(121, 21);
            this.ComPortDropdown.TabIndex = 0;
            this.ComPortDropdown.Text = "Com Ports";
            this.ComPortDropdown.SelectedIndexChanged += new System.EventHandler(this.ComPortDropdown_SelectedIndexChanged);
            // 
            // ComConnect
            // 
            this.ComConnect.Location = new System.Drawing.Point(12, 98);
            this.ComConnect.Name = "ComConnect";
            this.ComConnect.Size = new System.Drawing.Size(120, 23);
            this.ComConnect.TabIndex = 6;
            this.ComConnect.Text = "Connect";
            this.ComConnect.UseVisualStyleBackColor = true;
            this.ComConnect.Click += new System.EventHandler(this.ComConnect_Click);
            // 
            // ComDisconnect
            // 
            this.ComDisconnect.Location = new System.Drawing.Point(12, 127);
            this.ComDisconnect.Name = "ComDisconnect";
            this.ComDisconnect.Size = new System.Drawing.Size(120, 23);
            this.ComDisconnect.TabIndex = 7;
            this.ComDisconnect.Text = "Disconnect";
            this.ComDisconnect.UseVisualStyleBackColor = true;
            this.ComDisconnect.Click += new System.EventHandler(this.ComDisconnect_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.configurationToolStripMenuItem,
            this.toolStripMenuItem1});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(395, 24);
            this.menuStrip1.TabIndex = 9;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // configurationToolStripMenuItem
            // 
            this.configurationToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.configureHelmholtzCoilToolStripMenuItem,
            this.configureComPortToolStripMenuItem});
            this.configurationToolStripMenuItem.Name = "configurationToolStripMenuItem";
            this.configurationToolStripMenuItem.Size = new System.Drawing.Size(93, 20);
            this.configurationToolStripMenuItem.Text = "Configuration";
            //this.configurationToolStripMenuItem.Click += new System.EventHandler(this.configurationToolStripMenuItem_Click);
            // 
            // configureHelmholtzCoilToolStripMenuItem
            // 
            this.configureHelmholtzCoilToolStripMenuItem.Name = "configureHelmholtzCoilToolStripMenuItem";
            this.configureHelmholtzCoilToolStripMenuItem.Size = new System.Drawing.Size(217, 22);
            this.configureHelmholtzCoilToolStripMenuItem.Text = "Calibrate to Helmholtz Coil";
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.helpFileToolStripMenuItem,
            this.aboutSerialCatcherToolStripMenuItem});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(44, 20);
            this.toolStripMenuItem1.Text = "Help";
            // 
            // helpFileToolStripMenuItem
            // 
            this.helpFileToolStripMenuItem.Name = "helpFileToolStripMenuItem";
            this.helpFileToolStripMenuItem.Size = new System.Drawing.Size(182, 22);
            this.helpFileToolStripMenuItem.Text = "Help File";
            // 
            // aboutSerialCatcherToolStripMenuItem
            // 
            this.aboutSerialCatcherToolStripMenuItem.Name = "aboutSerialCatcherToolStripMenuItem";
            this.aboutSerialCatcherToolStripMenuItem.Size = new System.Drawing.Size(182, 22);
            this.aboutSerialCatcherToolStripMenuItem.Text = "About Serial Catcher";
            // 
            // lblStatus
            // 
            this.lblStatus.AutoSize = true;
            this.lblStatus.Location = new System.Drawing.Point(6, 16);
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(59, 13);
            this.lblStatus.TabIndex = 10;
            this.lblStatus.Text = "App Status";
            // 
            // serialPort1
            // 
            this.serialPort1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.serialPort1_DataReceived);
            // 
            // groupBox1
            // 
            this.groupBox1.AutoSize = true;
            this.groupBox1.Controls.Add(this.lblStatus);
            this.groupBox1.Location = new System.Drawing.Point(139, 31);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(245, 119);
            this.groupBox1.TabIndex = 11;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Information";
            // 
            // configureComPortToolStripMenuItem
            // 
            this.configureComPortToolStripMenuItem.Name = "configureComPortToolStripMenuItem";
            this.configureComPortToolStripMenuItem.Size = new System.Drawing.Size(217, 22);
            this.configureComPortToolStripMenuItem.Text = "Configure Com port";
            this.configureComPortToolStripMenuItem.Click += new System.EventHandler(this.configureComPortToolStripMenuItem_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(395, 170);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.ComDisconnect);
            this.Controls.Add(this.ComConnect);
            this.Controls.Add(this.ComPortDropdown);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.Text = "Serial Catcher";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox ComPortDropdown;
        private System.Windows.Forms.Button ComConnect;
        private System.Windows.Forms.Button ComDisconnect;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label lblStatus;
        private System.IO.Ports.SerialPort serialPort1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem helpFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutSerialCatcherToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem configurationToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem configureHelmholtzCoilToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem configureComPortToolStripMenuItem;
    }
}

