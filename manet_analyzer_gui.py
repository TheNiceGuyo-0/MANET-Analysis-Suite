#!/usr/bin/env python3
"""
MANET Security Simulation Results Analyzer - Professional GUI Version

A professional, well-organized graphical interface for analyzing MANET simulation results.
Features improved layout, styling, and result presentation.

Author: MANET Research Team
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Import the analyzer class
try:
    from manet_analyzer import MANETAnalyzer
except ImportError:
    print("Error: manet_analyzer.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

class ProfessionalMANETGUI:
    """
    Professional Graphical User Interface for MANET Simulation Analysis.
    
    Features a clean, organized layout with separated sections for different
    types of analysis results and improved visual presentation.
    """
    
    def __init__(self, root):
        """Initialize the professional GUI application."""
        self.root = root
        self.root.title("🛡️ MANET Security Analysis Suite - Professional Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configure styling
        self.setup_styles()
        
        # Initialize analyzer
        self.analyzer = None
        self.loaded_files = []
        self.analysis_results = {}
        
        # Create professional interface
        self.create_widgets()
        self.setup_layout()
        
        # Status
        self.update_status("🔧 Ready - Load simulation files to begin analysis", "info")
    
    def setup_styles(self):
        """Configure professional styling."""
        self.style = ttk.Style()
        
        # Try to use a modern theme
        try:
            available_themes = self.style.theme_names()
            if 'clam' in available_themes:
                self.style.theme_use('clam')
        except:
            pass
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('Success.TLabel', foreground='#2E7D32')
        self.style.configure('Error.TLabel', foreground='#C62828')
        self.style.configure('Warning.TLabel', foreground='#F57C00')
        self.style.configure('Info.TLabel', foreground='#1565C0')
        
        # Button styles
        self.style.configure('Action.TButton', font=('Arial', 9, 'bold'))
        
    def create_widgets(self):
        """Create all GUI widgets with professional organization."""
        
        # Main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="MANET Security Analysis Suite", 
                               style='Title.TLabel')
        title_label.pack(side="left")
        
        self.timestamp_label = ttk.Label(header_frame, text="", font=('Arial', 8))
        self.timestamp_label.pack(side="right")
        self.update_timestamp()
        
        # Main content area with paned window
        self.main_paned = ttk.PanedWindow(main_container, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True)
        
        # Left panel for controls
        self.left_panel = ttk.Frame(self.main_paned, width=400)
        self.main_paned.add(self.left_panel, weight=1)
        
        # Right panel for results
        self.right_panel = ttk.Frame(self.main_paned, width=800)
        self.main_paned.add(self.right_panel, weight=2)
        
        self.create_left_panel()
        self.create_right_panel()
        self.create_status_bar()
    
    def create_left_panel(self):
        """Create the left control panel."""
        # File Management Section
        file_section = ttk.LabelFrame(self.left_panel, text="📁 File Management", 
                                     padding=10)
        file_section.pack(fill="x", pady=(0, 10))
        
        # File operation buttons
        file_btn_frame = ttk.Frame(file_section)
        file_btn_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Button(file_btn_frame, text="➕ Add Files", 
                  command=self.add_files, style='Action.TButton').pack(side="left", padx=(0, 5))
        ttk.Button(file_btn_frame, text="📂 Add Folder", 
                  command=self.add_folder).pack(side="left", padx=(0, 5))
        ttk.Button(file_btn_frame, text="🗑️ Clear All", 
                  command=self.clear_files).pack(side="left")
        
        # File list with better formatting
        ttk.Label(file_section, text="Loaded Files:", style='Header.TLabel').pack(anchor="w", pady=(10, 2))
        
        list_frame = ttk.Frame(file_section)
        list_frame.pack(fill="both", expand=True)
        
        # Treeview for better file display
        self.file_tree = ttk.Treeview(list_frame, columns=('size', 'status'), 
                                     show='tree headings', height=6)
        self.file_tree.heading('#0', text='File Name')
        self.file_tree.heading('size', text='Size')
        self.file_tree.heading('status', text='Status')
        self.file_tree.column('#0', width=200)
        self.file_tree.column('size', width=60, anchor='center')
        self.file_tree.column('status', width=80, anchor='center')
        
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # Output Settings Section
        output_section = ttk.LabelFrame(self.left_panel, text="⚙️ Output Settings", 
                                       padding=10)
        output_section.pack(fill="x", pady=(0, 10))
        
        ttk.Label(output_section, text="Output Directory:", style='Header.TLabel').pack(anchor="w")
        dir_frame = ttk.Frame(output_section)
        dir_frame.pack(fill="x", pady=(2, 10))
        
        self.output_dir = tk.StringVar(value="analysis_output")
        ttk.Entry(dir_frame, textvariable=self.output_dir, font=('Arial', 9)).pack(side="left", fill="x", expand=True)
        ttk.Button(dir_frame, text="📁", command=self.browse_output_dir, width=3).pack(side="right", padx=(5,0))
        
        # Analysis Options Section
        options_section = ttk.LabelFrame(self.left_panel, text="📊 Analysis Options", 
                                        padding=10)
        options_section.pack(fill="x", pady=(0, 10))
        
        # Analysis type checkboxes
        self.generate_plots = tk.BooleanVar(value=True)
        self.generate_comparison = tk.BooleanVar(value=True)
        self.generate_report = tk.BooleanVar(value=True)
        self.export_data = tk.BooleanVar(value=True)
        
        options = [
            ("📈 Performance Plots", self.generate_plots),
            ("🔄 Comparison Analysis", self.generate_comparison),
            ("📄 Detailed Report", self.generate_report),
            ("💾 Export Data", self.export_data)
        ]
        
        for text, var in options:
            ttk.Checkbutton(options_section, text=text, variable=var).pack(anchor="w", pady=1)
        
        # Report format
        format_frame = ttk.Frame(options_section)
        format_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(format_frame, text="Report Format:", style='Header.TLabel').pack(side="left")
        self.report_format = tk.StringVar(value="html")
        format_combo = ttk.Combobox(format_frame, textvariable=self.report_format, 
                                   values=["html", "markdown", "txt"], state="readonly", width=8)
        format_combo.pack(side="right")
        
        # Action Buttons Section
        action_section = ttk.LabelFrame(self.left_panel, text="🚀 Actions", 
                                       padding=10)
        action_section.pack(fill="x")
        
        # Main action buttons
        ttk.Button(action_section, text="🔍 Run Full Analysis", 
                  command=self.run_full_analysis, style='Action.TButton').pack(fill="x", pady=2)
        ttk.Button(action_section, text="📊 Quick Statistics", 
                  command=self.show_quick_stats).pack(fill="x", pady=2)
        ttk.Button(action_section, text="📈 Generate Plots Only", 
                  command=self.generate_plots_only).pack(fill="x", pady=2)
        
        # Utility buttons
        util_frame = ttk.Frame(action_section)
        util_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(util_frame, text="📁 Open Output", 
                  command=self.open_output_folder).pack(side="left", fill="x", expand=True, padx=(0, 2))
        ttk.Button(util_frame, text="🗑️ Clear Results", 
                  command=self.clear_all_results).pack(side="right", fill="x", expand=True, padx=(2, 0))
    
    def create_right_panel(self):
        """Create the right results panel with organized sections."""
        # Results notebook for organized display
        self.results_notebook = ttk.Notebook(self.right_panel)
        self.results_notebook.pack(fill="both", expand=True)
        
        # === SUMMARY TAB ===
        self.summary_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.summary_frame, text="📋 Summary")
        
        # Summary content with scrollable text
        summary_container = ttk.Frame(self.summary_frame)
        summary_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.summary_text = scrolledtext.ScrolledText(summary_container, 
                                                     font=('Consolas', 10),
                                                     wrap=tk.WORD)
        self.summary_text.pack(fill="both", expand=True)
        
        # === STATISTICS TAB ===
        self.stats_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.stats_frame, text="📊 Statistics")
        
        # Statistics container
        stats_container = ttk.Frame(self.stats_frame)
        stats_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(stats_container, 
                                                   font=('Consolas', 9),
                                                   wrap=tk.WORD)
        self.stats_text.pack(fill="both", expand=True)
        
        # === DETAILED LOG TAB ===
        self.log_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.log_frame, text="📝 Detailed Log")
        
        log_container = ttk.Frame(self.log_frame)
        log_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_container, 
                                                 font=('Consolas', 9),
                                                 wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
        
        # === VISUALIZATION TAB ===
        self.viz_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.viz_frame, text="📈 Visualizations")
        
        viz_container = ttk.Frame(self.viz_frame)
        viz_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Visualization controls
        viz_controls = ttk.LabelFrame(viz_container, text="Plot Controls", padding=10)
        viz_controls.pack(fill="x", pady=(0, 10))
        
        control_buttons = ttk.Frame(viz_controls)
        control_buttons.pack(fill="x")
        
        ttk.Button(control_buttons, text="🎨 Generate Performance Plots", 
                  command=self.generate_performance_plots).pack(side="left", padx=(0, 5))
        ttk.Button(control_buttons, text="📊 Generate Comparison Plots", 
                  command=self.generate_comparison_plots).pack(side="left", padx=(0, 5))
        ttk.Button(control_buttons, text="🖼️ View Plot Gallery", 
                  command=self.open_plot_gallery).pack(side="left", padx=(0, 5))
        ttk.Button(control_buttons, text="📁 Open Plots Folder", 
                  command=self.open_plots_folder).pack(side="right")
        
        # Plot list and info
        viz_info = ttk.LabelFrame(viz_container, text="Generated Plots & Information", padding=10)
        viz_info.pack(fill="both", expand=True)
        
        # Create a frame for plot list and preview
        plot_frame = ttk.Frame(viz_info)
        plot_frame.pack(fill="both", expand=True)
        
        # Left side: Plot list
        list_frame = ttk.Frame(plot_frame)
        list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ttk.Label(list_frame, text="Generated Plot Files:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        self.plot_listbox = tk.Listbox(list_frame, font=('Arial', 9))
        plot_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.plot_listbox.yview)
        self.plot_listbox.configure(yscrollcommand=plot_scroll.set)
        self.plot_listbox.bind('<<ListboxSelect>>', self.on_plot_select)
        
        self.plot_listbox.pack(side="left", fill="both", expand=True)
        plot_scroll.pack(side="right", fill="y")
        
        # Right side: Plot info
        info_frame = ttk.Frame(plot_frame)
        info_frame.pack(side="right", fill="both", expand=True)
        
        ttk.Label(info_frame, text="Plot Information:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        self.plot_info_text = scrolledtext.ScrolledText(info_frame, 
                                                       font=('Arial', 9),
                                                       height=12, width=40)
        self.plot_info_text.pack(fill="both", expand=True)
        
        # Status and log area
        viz_log_frame = ttk.LabelFrame(viz_container, text="Visualization Log", padding=5)
        viz_log_frame.pack(fill="x", pady=(10, 0))
        
        self.viz_text = scrolledtext.ScrolledText(viz_log_frame, 
                                                 font=('Consolas', 9),
                                                 height=6)
        self.viz_text.pack(fill="both", expand=True)
    
    def create_status_bar(self):
        """Create professional status bar."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 5))
        
        # Status label with icon
        status_container = ttk.Frame(self.status_frame)
        status_container.pack(fill="x")
        
        self.status_icon = ttk.Label(status_container, text="ℹ️")
        self.status_icon.pack(side="left", padx=(0, 5))
        
        self.status_label = ttk.Label(status_container, text="Ready", style='Info.TLabel')
        self.status_label.pack(side="left", fill="x", expand=True)
        
        # Progress bar (hidden initially)
        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        
        # File count label
        self.file_count_label = ttk.Label(status_container, text="Files: 0", 
                                         font=('Arial', 8))
        self.file_count_label.pack(side="right")
    
    def setup_layout(self):
        """Setup professional layout."""
        # Start with summary tab selected
        self.results_notebook.select(0)
    
    def update_timestamp(self):
        """Update timestamp in header."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Session: {current_time}")
        
        # Schedule next update
        self.root.after(60000, self.update_timestamp)  # Update every minute
    
    def update_status(self, message, status_type="info"):
        """Update status bar with appropriate styling."""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "working": "⚙️"
        }
        
        styles = {
            "info": "Info.TLabel",
            "success": "Success.TLabel",
            "warning": "Warning.TLabel",
            "error": "Error.TLabel",
            "working": "Info.TLabel"
        }
        
        self.status_icon.config(text=icons.get(status_type, "ℹ️"))
        self.status_label.config(text=message, style=styles.get(status_type, "Info.TLabel"))
        self.root.update_idletasks()
    
    def add_files(self):
        """Add individual files with better tracking."""
        files = filedialog.askopenfilenames(
            title="Select MANET Simulation Result Files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        added_count = 0
        for file_path in files:
            if file_path not in self.loaded_files:
                self.loaded_files.append(file_path)
                
                # Add to tree view with file info
                file_name = os.path.basename(file_path)
                file_size = self.get_file_size(file_path)
                
                self.file_tree.insert("", "end", text=file_name, 
                                     values=(file_size, "Ready"))
                added_count += 1
        
        self.update_file_count()
        if added_count > 0:
            self.update_status(f"Added {added_count} files", "success")
        else:
            self.update_status("No new files added", "warning")
    
    def add_folder(self):
        """Add folder with better feedback."""
        folder = filedialog.askdirectory(title="Select Folder with Simulation Results")
        
        if folder:
            json_files = list(Path(folder).glob("*.json"))
            added_count = 0
            
            for file_path in json_files:
                file_str = str(file_path)
                if file_str not in self.loaded_files:
                    self.loaded_files.append(file_str)
                    
                    file_size = self.get_file_size(file_str)
                    self.file_tree.insert("", "end", text=file_path.name, 
                                         values=(file_size, "Ready"))
                    added_count += 1
            
            self.update_file_count()
            if added_count > 0:
                self.update_status(f"Added {added_count} files from folder", "success")
            else:
                self.update_status("No new JSON files found in folder", "warning")
    
    def clear_files(self):
        """Clear all files with confirmation."""
        if self.loaded_files:
            if messagebox.askyesno("Confirm Clear", 
                                  f"Clear all {len(self.loaded_files)} loaded files?"):
                self.loaded_files.clear()
                self.file_tree.delete(*self.file_tree.get_children())
                self.analyzer = None
                self.update_file_count()
                self.update_status("All files cleared", "info")
        else:
            self.update_status("No files to clear", "info")
    
    def get_file_size(self, file_path):
        """Get formatted file size."""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size}B"
            elif size < 1024*1024:
                return f"{size/1024:.1f}KB"
            else:
                return f"{size/(1024*1024):.1f}MB"
        except:
            return "N/A"
    
    def update_file_count(self):
        """Update file count display."""
        count = len(self.loaded_files)
        self.file_count_label.config(text=f"Files: {count}")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.update_status(f"Output directory set to: {os.path.basename(directory)}", "info")
    
    def initialize_analyzer(self):
        """Initialize analyzer with better error handling."""
        if not self.loaded_files:
            self.update_status("No files loaded", "error")
            messagebox.showerror("Error", "No files loaded. Please add simulation files first.")
            return False
        
        try:
            self.update_status("Initializing analyzer...", "working")
            self.analyzer = MANETAnalyzer(self.output_dir.get())
            
            loaded_count = 0
            failed_files = []
            
            # Update file tree status
            for i, (file_path, item) in enumerate(zip(self.loaded_files, self.file_tree.get_children())):
                self.file_tree.set(item, 'status', 'Loading...')
                self.root.update_idletasks()
                
                success = self.analyzer.load_simulation(file_path)
                if success:
                    self.file_tree.set(item, 'status', 'Loaded ✓')
                    loaded_count += 1
                else:
                    self.file_tree.set(item, 'status', 'Failed ✗')
                    failed_files.append(os.path.basename(file_path))
            
            if not self.analyzer.simulations:
                self.update_status("No valid simulations loaded", "error")
                messagebox.showerror("Error", "No valid simulation files could be loaded.")
                return False
            
            # Log initialization results
            self.log_message(f"Analyzer initialized successfully")
            self.log_message(f"✅ Loaded: {loaded_count} simulations")
            if failed_files:
                self.log_message(f"❌ Failed to load: {', '.join(failed_files)}")
            
            self.update_status(f"Analyzer ready - {loaded_count} simulations loaded", "success")
            return True
            
        except Exception as e:
            self.update_status("Analyzer initialization failed", "error")
            messagebox.showerror("Error", f"Failed to initialize analyzer: {str(e)}")
            return False
    
    def run_full_analysis(self):
        """Run comprehensive analysis with professional progress tracking."""
        if not self.initialize_analyzer():
            return
        
        # Clear previous results
        self.clear_all_results()
        
        # Start progress
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.start()
        
        # Run in thread
        thread = threading.Thread(target=self._run_full_analysis_thread, daemon=True)
        thread.start()
    
    def _run_full_analysis_thread(self):
        """Professional analysis thread with detailed progress."""
        try:
            self.update_status("Running comprehensive analysis...", "working")
            self.log_message("=" * 70)
            self.log_message("🚀 COMPREHENSIVE ANALYSIS STARTED")
            self.log_message(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.log_message("=" * 70)
            
            results = {}
            
            # Generate plots
            if self.generate_plots.get():
                self.update_status("Generating performance plots...", "working")
                self.log_message("📊 Generating performance plots...")
                try:
                    plot_files = self.analyzer.generate_performance_plots(save=True)
                    results['plots'] = plot_files
                    self.log_message("✅ Performance plots generated successfully")
                    
                    # Add to visualization tab
                    if plot_files:
                        for plot_file in plot_files:
                            plot_name = os.path.basename(str(plot_file))
                            self.plot_listbox.insert(tk.END, plot_name)
                        self.viz_message("📈 Performance plots generated and added to gallery")
                        
                except Exception as e:
                    self.log_message(f"❌ Plot generation failed: {str(e)}")
            
            # Generate comparisons
            if self.generate_comparison.get():
                if len(self.analyzer.simulations) > 1:
                    self.update_status("Generating comparison analysis...", "working")
                    self.log_message("🔄 Generating comparison analysis...")
                    try:
                        comparison_files = self.analyzer.compare_simulations(save=True)
                        results['comparisons'] = comparison_files
                        self.log_message("✅ Comparison analysis completed")
                        
                        # Add to visualization tab
                        if comparison_files:
                            for comp_file in comparison_files:
                                plot_name = os.path.basename(str(comp_file))
                                self.plot_listbox.insert(tk.END, f"[COMP] {plot_name}")
                            self.viz_message("📊 Comparison plots generated and added to gallery")
                            
                    except Exception as e:
                        self.log_message(f"❌ Comparison analysis failed: {str(e)}")
                else:
                    self.log_message("⚠️ Comparison requires at least 2 simulations")
            
            # Generate report
            if self.generate_report.get():
                self.update_status("Generating detailed report...", "working")
                self.log_message("📄 Generating analysis report...")
                try:
                    report_file = self.analyzer.generate_report(
                        output_format=self.report_format.get(),
                        include_plots=self.generate_plots.get()
                    )
                    results['report'] = report_file
                    self.log_message(f"✅ Report generated: {report_file.name}")
                except Exception as e:
                    self.log_message(f"❌ Report generation failed: {str(e)}")
            
            # Export data
            if self.export_data.get():
                self.update_status("Exporting processed data...", "working")
                self.log_message("💾 Exporting processed data...")
                try:
                    data_file = self.analyzer.export_processed_data()
                    results['data'] = data_file
                    self.log_message(f"✅ Data exported: {data_file.name}")
                except Exception as e:
                    self.log_message(f"❌ Data export failed: {str(e)}")
            
            # Generate comprehensive summary
            self.update_status("Generating summary statistics...", "working")
            self.generate_comprehensive_summary()
            
            # Store results
            self.analysis_results = results
            
            self.log_message("=" * 70)
            self.log_message("🎉 ANALYSIS COMPLETED SUCCESSFULLY")
            self.log_message("=" * 70)
            
            self.update_status("Analysis completed successfully! Check results tabs.", "success")
            
        except Exception as e:
            self.log_message(f"💥 CRITICAL ERROR: Analysis failed - {str(e)}")
            self.update_status("Analysis failed - check log for details", "error")
        
        finally:
            # Stop progress
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def generate_comprehensive_summary(self):
        """Generate a comprehensive, professional summary."""
        try:
            summary_stats = self.analyzer.get_summary_statistics()
            
            # Clear and populate summary
            self.summary_text.delete(1.0, tk.END)
            
            # Header
            self.summary_text.insert(tk.END, "🛡️ MANET SECURITY ANALYSIS SUMMARY\n")
            self.summary_text.insert(tk.END, "=" * 60 + "\n\n")
            
            # Overview
            self.summary_text.insert(tk.END, f"📊 Analysis Overview:\n")
            self.summary_text.insert(tk.END, f"   • Total Simulations: {len(summary_stats)}\n")
            self.summary_text.insert(tk.END, f"   • Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.summary_text.insert(tk.END, f"   • Output Directory: {self.output_dir.get()}\n\n")
            
            # Simulation details
            for i, (label, stats) in enumerate(summary_stats.items(), 1):
                self.summary_text.insert(tk.END, f"🔹 Simulation {i}: {label}\n")
                self.summary_text.insert(tk.END, f"   📈 Data Points: {stats['data_points']:,}\n")
                
                config = stats['configuration']
                self.summary_text.insert(tk.END, f"   ⚙️ Configuration:\n")
                for key, value in config.items():
                    self.summary_text.insert(tk.END, f"      • {key.replace('_', ' ').title()}: {value}\n")
                
                self.summary_text.insert(tk.END, f"   📊 Key Metrics:\n")
                for metric, values in stats['metrics'].items():
                    if isinstance(values, dict) and 'mean' in values:
                        self.summary_text.insert(tk.END, 
                            f"      • {metric.replace('_', ' ').title()}: "
                            f"Mean={values['mean']:.4f}, Std={values['std']:.4f}\n")
                
                self.summary_text.insert(tk.END, "\n")
            
            # Generate detailed statistics
            self.generate_detailed_statistics(summary_stats)
            
        except Exception as e:
            self.summary_text.insert(tk.END, f"❌ Error generating summary: {str(e)}\n")
    
    def generate_detailed_statistics(self, summary_stats):
        """Generate detailed statistics in separate tab."""
        try:
            self.stats_text.delete(1.0, tk.END)
            
            self.stats_text.insert(tk.END, "📊 DETAILED STATISTICAL ANALYSIS\n")
            self.stats_text.insert(tk.END, "=" * 70 + "\n\n")
            
            for label, stats in summary_stats.items():
                self.stats_text.insert(tk.END, f"📈 SIMULATION: {label.upper()}\n")
                self.stats_text.insert(tk.END, "-" * 50 + "\n")
                
                # Configuration table
                self.stats_text.insert(tk.END, "Configuration Parameters:\n")
                config = stats['configuration']
                for key, value in config.items():
                    self.stats_text.insert(tk.END, f"  {key.ljust(25)}: {value}\n")
                
                self.stats_text.insert(tk.END, "\nPerformance Metrics:\n")
                self.stats_text.insert(tk.END, f"{'Metric'.ljust(20)} {'Mean'.ljust(12)} {'Std'.ljust(12)} {'Min'.ljust(12)} {'Max'.ljust(12)}\n")
                self.stats_text.insert(tk.END, "-" * 70 + "\n")
                
                for metric, values in stats['metrics'].items():
                    if isinstance(values, dict) and 'mean' in values:
                        self.stats_text.insert(tk.END, 
                            f"{metric.ljust(20)} "
                            f"{values['mean']:.6f}".ljust(12) + " "
                            f"{values['std']:.6f}".ljust(12) + " "
                            f"{values['min']:.6f}".ljust(12) + " "
                            f"{values['max']:.6f}".ljust(12) + "\n")
                
                self.stats_text.insert(tk.END, "\n\n")
                
        except Exception as e:
            self.stats_text.insert(tk.END, f"❌ Error generating detailed statistics: {str(e)}\n")
    
    def show_quick_stats(self):
        """Show quick statistics with professional formatting."""
        if not self.initialize_analyzer():
            return
        
        try:
            self.update_status("Calculating quick statistics...", "working")
            summary_stats = self.analyzer.get_summary_statistics()
            
            # Clear and show in summary tab
            self.summary_text.delete(1.0, tk.END)
            self.results_notebook.select(0)  # Switch to summary tab
            
            self.summary_text.insert(tk.END, "⚡ QUICK STATISTICS OVERVIEW\n")
            self.summary_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for i, (label, stats) in enumerate(summary_stats.items(), 1):
                self.summary_text.insert(tk.END, f"🔸 Simulation {i}: {label}\n")
                self.summary_text.insert(tk.END, f"   Data Points: {stats['data_points']:,}\n")
                self.summary_text.insert(tk.END, f"   Nodes: {stats['configuration'].get('num_nodes', 'N/A')}\n")
                
                # Show top 3 metrics
                metrics_shown = 0
                for metric, values in stats['metrics'].items():
                    if metrics_shown >= 3:
                        break
                    if isinstance(values, dict) and 'mean' in values:
                        self.summary_text.insert(tk.END, 
                            f"   {metric.replace('_', ' ').title()}: {values['mean']:.4f}\n")
                        metrics_shown += 1
                
                self.summary_text.insert(tk.END, "\n")
            
            self.update_status("Quick statistics completed", "success")
            
        except Exception as e:
            self.summary_text.insert(tk.END, f"❌ Statistics calculation failed: {str(e)}\n")
            self.update_status("Statistics calculation failed", "error")
    
    def generate_performance_plots(self):
        """Generate performance plots with improved visualization."""
        if not self.initialize_analyzer():
            return
        
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.start()
        self.update_status("Generating performance plots...", "working")
        
        thread = threading.Thread(target=self._generate_performance_plots_thread, daemon=True)
        thread.start()
    
    def _generate_performance_plots_thread(self):
        """Generate performance plots in background."""
        try:
            self.viz_message("🎨 Starting performance plot generation...")
            self.results_notebook.select(3)  # Switch to visualization tab
            
            # Generate plots with improved settings
            plot_files = self.analyzer.generate_performance_plots(save=True)
            
            if plot_files:
                self.viz_message("✅ Performance plots generated successfully!")
                for plot_file in plot_files:
                    plot_name = os.path.basename(str(plot_file))
                    self.plot_listbox.insert(tk.END, plot_name)
                    self.viz_message(f"   📊 {plot_name}")
                
                # Auto-select first plot
                if self.plot_listbox.size() > 0:
                    self.plot_listbox.selection_set(0)
                    self.on_plot_select(None)
            else:
                self.viz_message("⚠️ No plot files were generated")
            
            self.update_status("Performance plots generated", "success")
            
        except Exception as e:
            self.viz_message(f"❌ Performance plot generation failed: {str(e)}")
            self.update_status("Plot generation failed", "error")
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def generate_comparison_plots(self):
        """Generate comparison plots."""
        if not self.initialize_analyzer():
            return
        
        if len(self.analyzer.simulations) < 2:
            messagebox.showwarning("Warning", "Comparison plots require at least 2 simulations.")
            return
        
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.start()
        self.update_status("Generating comparison plots...", "working")
        
        thread = threading.Thread(target=self._generate_comparison_plots_thread, daemon=True)
        thread.start()
    
    def _generate_comparison_plots_thread(self):
        """Generate comparison plots in background."""
        try:
            self.viz_message("🔄 Starting comparison plot generation...")
            self.results_notebook.select(3)  # Switch to visualization tab
            
            comparison_files = self.analyzer.compare_simulations(save=True)
            
            if comparison_files:
                self.viz_message("✅ Comparison plots generated successfully!")
                for comp_file in comparison_files:
                    plot_name = os.path.basename(str(comp_file))
                    self.plot_listbox.insert(tk.END, f"[COMP] {plot_name}")
                    self.viz_message(f"   📈 {plot_name}")
            else:
                self.viz_message("⚠️ No comparison files were generated")
            
            self.update_status("Comparison plots generated", "success")
            
        except Exception as e:
            self.viz_message(f"❌ Comparison plot generation failed: {str(e)}")
            self.update_status("Comparison plot generation failed", "error")
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def on_plot_select(self, event):
        """Handle plot selection to show plot information."""
        selection = self.plot_listbox.curselection()
        if not selection:
            return
        
        plot_name = self.plot_listbox.get(selection[0])
        
        # Clean up plot name
        if plot_name.startswith("[COMP] "):
            clean_name = plot_name[7:]
            plot_type = "Comparison Plot"
        else:
            clean_name = plot_name
            plot_type = "Performance Plot"
        
        # Get plot file path
        plot_path = Path(self.output_dir.get()) / clean_name
        
        # Display plot information
        self.plot_info_text.delete(1.0, tk.END)
        self.plot_info_text.insert(tk.END, f"📊 {plot_type}\n")
        self.plot_info_text.insert(tk.END, "=" * 30 + "\n\n")
        self.plot_info_text.insert(tk.END, f"File: {clean_name}\n")
        self.plot_info_text.insert(tk.END, f"Path: {plot_path}\n\n")
        
        if plot_path.exists():
            try:
                file_size = plot_path.stat().st_size
                size_mb = file_size / (1024 * 1024)
                self.plot_info_text.insert(tk.END, f"Size: {size_mb:.2f} MB\n")
                
                mod_time = datetime.fromtimestamp(plot_path.stat().st_mtime)
                self.plot_info_text.insert(tk.END, f"Created: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                self.plot_info_text.insert(tk.END, "📝 Description:\n")
                if "performance" in clean_name.lower():
                    self.plot_info_text.insert(tk.END, "• Shows key performance metrics over time\n")
                    self.plot_info_text.insert(tk.END, "• Includes throughput, delay, and trust scores\n")
                elif "comparison" in clean_name.lower():
                    self.plot_info_text.insert(tk.END, "• Compares multiple simulation runs\n")
                    self.plot_info_text.insert(tk.END, "• Shows relative performance differences\n")
                elif "correlation" in clean_name.lower():
                    self.plot_info_text.insert(tk.END, "• Shows metric correlations\n")
                    self.plot_info_text.insert(tk.END, "• Helps identify relationships\n")
                
                self.plot_info_text.insert(tk.END, "\n💡 Tip: Use 'Open Plots Folder' to view the actual plot files")
                
            except Exception as e:
                self.plot_info_text.insert(tk.END, f"Error reading file info: {str(e)}")
        else:
            self.plot_info_text.insert(tk.END, "❌ File not found")
    
    def open_plot_gallery(self):
        """Open a simple plot gallery window."""
        output_path = Path(self.output_dir.get())
        plot_files = list(output_path.glob("*.png")) + list(output_path.glob("*.jpg")) + list(output_path.glob("*.svg"))
        
        if not plot_files:
            messagebox.showinfo("No Plots", "No plot files found. Generate some plots first!")
            return
        
        # Create gallery window
        gallery_window = tk.Toplevel(self.root)
        gallery_window.title("📊 Plot Gallery")
        gallery_window.geometry("600x400")
        
        # Gallery content
        gallery_frame = ttk.Frame(gallery_window)
        gallery_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(gallery_frame, text="🖼️ Generated Plots Gallery", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Plot list
        plot_list_frame = ttk.LabelFrame(gallery_frame, text="Available Plots", padding=10)
        plot_list_frame.pack(fill="both", expand=True)
        
        gallery_listbox = tk.Listbox(plot_list_frame, font=('Arial', 10))
        gallery_scroll = ttk.Scrollbar(plot_list_frame, orient="vertical", command=gallery_listbox.yview)
        gallery_listbox.configure(yscrollcommand=gallery_scroll.set)
        
        for plot_file in plot_files:
            gallery_listbox.insert(tk.END, plot_file.name)
        
        gallery_listbox.pack(side="left", fill="both", expand=True)
        gallery_scroll.pack(side="right", fill="y")
        
        # Buttons
        button_frame = ttk.Frame(gallery_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        def open_selected_plot():
            selection = gallery_listbox.curselection()
            if selection:
                plot_name = gallery_listbox.get(selection[0])
                plot_path = output_path / plot_name
                self.open_file_with_system(plot_path)
        
        ttk.Button(button_frame, text="🖼️ Open Selected Plot", 
                  command=open_selected_plot).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="📁 Open Plots Folder", 
                  command=self.open_plots_folder).pack(side="left")
        ttk.Button(button_frame, text="❌ Close", 
                  command=gallery_window.destroy).pack(side="right")
    
    def open_plots_folder(self):
        """Open the plots folder specifically."""
        output_path = Path(self.output_dir.get())
        if output_path.exists():
            self.open_file_with_system(output_path)
            self.update_status(f"Opened plots folder", "success")
        else:
            messagebox.showwarning("Warning", "Output folder does not exist yet. Generate some plots first.")
    
    def open_file_with_system(self, file_path):
        """Open file or folder with system default application."""
        import subprocess
        import platform
        
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.run(["explorer", str(file_path)])
            elif system == "Darwin":
                subprocess.run(["open", str(file_path)])
            else:
                subprocess.run(["xdg-open", str(file_path)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")
    
    def clear_plot_list(self):
        """Clear the plot list."""
        self.plot_listbox.delete(0, tk.END)
        self.plot_info_text.delete(1.0, tk.END)
    
    def _generate_plots_thread(self):
        """Generate plots in background thread."""
        try:
            self.update_status("Generating visualization plots...", "working")
            self.viz_text.delete(1.0, tk.END)
            self.results_notebook.select(3)  # Switch to visualization tab
            
            self.viz_text.insert(tk.END, "📈 PLOT GENERATION LOG\n")
            self.viz_text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Generate performance plots
            self.viz_text.insert(tk.END, "🎨 Generating performance plots...\n")
            plot_files = self.analyzer.generate_performance_plots(save=True)
            
            if plot_files:
                self.viz_text.insert(tk.END, "✅ Performance plots generated:\n")
                for plot_file in plot_files:
                    self.viz_text.insert(tk.END, f"   📊 {plot_file}\n")
            
            # Generate comparison if possible
            if len(self.analyzer.simulations) > 1:
                self.viz_text.insert(tk.END, "\n🔄 Generating comparison plots...\n")
                comparison_files = self.analyzer.compare_simulations(save=True)
                
                if comparison_files:
                    self.viz_text.insert(tk.END, "✅ Comparison plots generated:\n")
                    for comp_file in comparison_files:
                        self.viz_text.insert(tk.END, f"   📈 {comp_file}\n")
            else:
                self.viz_text.insert(tk.END, "\n⚠️ Comparison plots require multiple simulations\n")
            
            self.viz_text.insert(tk.END, f"\n🎉 Plot generation completed successfully!\n")
            self.viz_text.insert(tk.END, f"📁 Plots saved to: {self.output_dir.get()}\n")
            
            self.update_status("Plot generation completed successfully", "success")
            
        except Exception as e:
            self.viz_text.insert(tk.END, f"\n❌ Plot generation failed: {str(e)}\n")
            self.update_status("Plot generation failed", "error")
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def log_message(self, message):
        """Add message to detailed log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def viz_message(self, message):
        """Add message to visualization log."""
        self.viz_text.insert(tk.END, f"{message}\n")
        self.viz_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_all_results(self):
        """Clear all result displays."""
        self.summary_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.viz_text.delete(1.0, tk.END)
        self.clear_plot_list()
        self.analysis_results = {}
    
    def generate_plots_only(self):
        """Generate both performance and comparison plots."""
        if not self.initialize_analyzer():
            return
        
        # Clear previous plots
        self.clear_plot_list()
        
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.start()
        
        thread = threading.Thread(target=self._generate_all_plots_thread, daemon=True)
        thread.start()
    
    def _generate_all_plots_thread(self):
        """Generate all plots in background thread."""
        try:
            self.update_status("Generating all visualization plots...", "working")
            self.viz_text.delete(1.0, tk.END)
            self.results_notebook.select(3)  # Switch to visualization tab
            
            self.viz_message("🎨 PLOT GENERATION SESSION STARTED")
            self.viz_message("=" * 50)
            
            # Generate performance plots
            self.viz_message("📊 Generating performance plots...")
            try:
                plot_files = self.analyzer.generate_performance_plots(save=True)
                
                if plot_files:
                    self.viz_message("✅ Performance plots generated successfully:")
                    for plot_file in plot_files:
                        plot_name = os.path.basename(str(plot_file))
                        self.plot_listbox.insert(tk.END, plot_name)
                        self.viz_message(f"   📈 {plot_name}")
                else:
                    self.viz_message("⚠️ No performance plot files generated")
                    
            except Exception as e:
                self.viz_message(f"❌ Performance plot generation failed: {str(e)}")
            
            # Generate comparison if possible
            if len(self.analyzer.simulations) > 1:
                self.viz_message("\n🔄 Generating comparison plots...")
                try:
                    comparison_files = self.analyzer.compare_simulations(save=True)
                    
                    if comparison_files:
                        self.viz_message("✅ Comparison plots generated successfully:")
                        for comp_file in comparison_files:
                            plot_name = os.path.basename(str(comp_file))
                            self.plot_listbox.insert(tk.END, f"[COMP] {plot_name}")
                            self.viz_message(f"   📊 {plot_name}")
                    else:
                        self.viz_message("⚠️ No comparison plot files generated")
                        
                except Exception as e:
                    self.viz_message(f"❌ Comparison plot generation failed: {str(e)}")
            else:
                self.viz_message("\n⚠️ Comparison plots require multiple simulations")
            
            # Final summary
            total_plots = self.plot_listbox.size()
            self.viz_message(f"\n🎉 Plot generation completed!")
            self.viz_message(f"📊 Total plots generated: {total_plots}")
            self.viz_message(f"📁 Plots saved to: {self.output_dir.get()}")
            
            if total_plots > 0:
                self.viz_message("\n💡 Tips:")
                self.viz_message("   • Select a plot from the list to view details")
                self.viz_message("   • Use 'Open Plots Folder' to view actual files")
                self.viz_message("   • Use 'View Plot Gallery' for easy browsing")
                
                # Auto-select first plot
                self.plot_listbox.selection_set(0)
                self.on_plot_select(None)
            
            self.update_status(f"Plot generation completed - {total_plots} plots generated", "success")
            
        except Exception as e:
            self.viz_message(f"\n💥 CRITICAL ERROR: Plot generation failed - {str(e)}")
            self.update_status("Plot generation failed", "error")
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def open_output_folder(self):
        """Open output folder with error handling."""
        output_path = Path(self.output_dir.get())
        
        if output_path.exists():
            import subprocess
            import platform
            
            try:
                system = platform.system()
                if system == "Windows":
                    subprocess.run(["explorer", str(output_path)])
                elif system == "Darwin":
                    subprocess.run(["open", str(output_path)])
                else:
                    subprocess.run(["xdg-open", str(output_path)])
                
                self.update_status(f"Opened output folder: {output_path.name}", "success")
                
            except Exception as e:
                self.update_status("Failed to open folder", "error")
                messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
        else:
            self.update_status("Output folder does not exist", "warning")
            messagebox.showwarning("Warning", "Output folder does not exist yet. Run analysis first.")

def main():
    """Main function to run the professional GUI application."""
    root = tk.Tk()
    
    # Configure window
    root.configure(bg='#f0f0f0')
    
    # Create and run application
    app = ProfessionalMANETGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Run application
    root.mainloop()

if __name__ == "__main__":
    main()