using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SerialDataExample
{
    public partial class ComportConfig : Form
    {
        public ComportConfig()
        {
            InitializeComponent();
        }

        private void ComPorts_SelectedIndexChanged(object sender, EventArgs e)
        {
            var ports = SerialPort.GetPortNames();
            ComPorts.DataSource = ports;
        }


    }
}
